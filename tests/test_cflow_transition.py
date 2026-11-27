import sys
from pathlib import Path

import numpy as np
import pytest
import torch

from dataset_generation.bytecode2cflow import make_examples
from pylingual.control_flow_reconstruction.model_view import INPUT_TOKENS, CflowRequest
from pylingual.control_flow_reconstruction.skeleton_template import SkeletonTemplate
from pylingual.control_flow_reconstruction.transition import CHAINS, FRAME_KINDS, MAX_DEPTH, SPECIAL, TOKENS, TransitionConfig, TransitionModel
from pylingual.decompiler import has_comp_error
from pylingual.editable_bytecode import PYCFile
from pylingual.models import TransitionPredictor, control_flow_config
from pylingual.utils.version import PythonVersion

from test_cflow_dataset import VERSIONS, compiled_fixture
from test_cflow_decompiler import cft_of_f, decompile_with


def tiny_model(seed=0, products=False) -> TransitionModel:
    torch.manual_seed(seed)
    return TransitionModel(TransitionConfig(vocab=[*SPECIAL, *INPUT_TOKENS, "K_stmt", "RETURN_CONST"], d_model=32, layers=1, heads=2, d_ff=64, products=products)).eval()


@pytest.mark.filterwarnings("ignore::SyntaxWarning")
@pytest.mark.parametrize("version", VERSIONS)
@pytest.mark.parametrize("fixture", ["Conditional", "Exception", "Loop", "Match", "With"])
def test_random_model_skeletons_are_accepted(fixture, version, tmp_path):
    """An untrained model's skeletons for real code objects are accepted by their grammar, distinct, and k at most."""
    src, pyc_path = compiled_fixture(fixture, PythonVersion(version), tmp_path)
    requests = [CflowRequest.from_row(e) for e in make_examples(PYCFile(str(pyc_path)), src)]
    predictor = TransitionPredictor(tiny_model())
    for k in (1, 3):
        results = predictor(requests, num_beams=k)
        assert all(results), "every request gets a skeleton"
        for request, skeletons in zip(requests, results):
            assert all(request.grammar().accepts(s) for s in skeletons)
            assert 1 <= len(skeletons) <= k and len({tuple(s) for s in skeletons}) == len(skeletons)


def test_save_load_and_decompile(tmp_path):
    """A saved model loads as the decompiler's control flow model, which takes its skeletons, right or not."""
    model = tiny_model(seed=1)
    model.config.max_stmts = 100
    model.save_pretrained(tmp_path / "model")
    loaded = TransitionPredictor.from_pretrained(str(tmp_path / "model"))
    assert loaded.model.config.max_stmts == 100 and loaded.model.config.vocab == model.config.vocab
    request = CflowRequest.from_row({"input": "| <s0> K_cond POP_JUMP_IF_FALSE f+ <s2> | <s1> K_stmt | <s2> K_stmt RETURN_CONST nf", "shapes": "cond stmt stmt", "version": "3.12"})
    assert loaded([request], num_beams=4) == TransitionPredictor(model)([request], num_beams=4)
    d = decompile_with(loaded, tmp_path)
    f = [bc.codeobj.co_name for bc in d.ordered_bytecodes].index("f")
    assert d.cflow_results[f] and all(d.cflow_requests[f].grammar().accepts(s) for s in d.cflow_results[f])
    # the untrained model's skeleton can be wrong, but it fits the grammar, so the source compiles
    assert isinstance(cft_of_f(d), SkeletonTemplate) and d.cflow_requests[f].grammar().accepts(cft_of_f(d).tokens)
    assert d.equivalence_results and not has_comp_error(d.equivalence_results)


def no_dropout(model: TransitionModel) -> TransitionModel:
    for module in model.modules():
        if isinstance(module, torch.nn.Dropout):
            module.p = 0.0
        if isinstance(module, torch.nn.MultiheadAttention):
            module.dropout = 0.0
    return model


def test_inference_encoder_is_the_training_encoder():
    """encode_inference gives the encoder states of the path the model trains with, at every real token of padded inputs."""
    model = no_dropout(tiny_model())
    torch.manual_seed(1)
    x = torch.randn(3, 48, model.config.d_model)
    mask = torch.ones(3, 48, dtype=torch.long)
    mask[1, 40:], mask[2, 7:] = 0, 0
    with torch.no_grad():
        trained = model.train().encoder(x, src_key_padding_mask=~mask.bool())
        inference = model.eval().encode_inference(x, mask)
    real = mask.bool()
    assert torch.allclose(trained[real], inference[real], atol=1e-5)


@pytest.mark.parametrize("products", [False, True])
def test_decode_step_is_the_teacher_forced_step(products):
    """One cached decoding step for k rows per request gives the logits of step_inputs and scores on repeated tensors."""
    model = tiny_model(products=products)
    requests = [
        CflowRequest.from_row({"input": "| <s0> K_cond POP_JUMP_IF_FALSE f+ <s2> | <s1> K_stmt | <s2> K_stmt RETURN_CONST nf", "shapes": "cond stmt stmt", "version": "3.12"}),
        CflowRequest.from_row({"input": "| <s0> K_stmt | <s1> K_stmt RETURN_CONST nf", "shapes": "stmt stmt", "version": "3.12"}),
    ]
    k, rows = 3, 6
    inputs = model.batch_inputs(requests)
    rng = np.random.default_rng(0)
    n = 3
    highs = [len(TOKENS) + 3, n, len(TOKENS) + 3, n, n, len(FRAME_KINDS), len(CHAINS), 8, MAX_DEPTH]
    feats_np = np.stack([rng.integers(-1 if i in (1, 3, 4) else 0, h, rows) for i, h in enumerate(highs)], -1)
    feats = torch.from_numpy(feats_np)[:, None]
    with torch.no_grad():
        memory, stmts = model.encode(**inputs)
        cached, _ = model.decode_step(model.decoding_cache(memory, stmts, inputs["attention_mask"]), feats_np, None, k)
        memory, stmts, mask = (t.repeat_interleave(k, 0) for t in (memory, stmts, inputs["attention_mask"]))
        h, _ = model.lstm(model.step_inputs(stmts, feats))
        reference = model.scores(h, memory, mask, stmts, feats[..., 4])[:, 0]
    assert torch.allclose(cached, reference, atol=1e-5)


def test_shared_control_flow_config():
    """A top-level CONTROL_FLOW_MODEL serves every version; a version's own entry overrides it."""
    shared, own = {"REPO": "unified"}, {"REPO": "py312"}
    config = {"v3.6": {}, "v3.12": {"CONTROL_FLOW_MODEL": own}}
    assert control_flow_config(config, PythonVersion((3, 6))) is None
    config["CONTROL_FLOW_MODEL"] = shared
    assert control_flow_config(config, PythonVersion((3, 6))) == shared
    assert control_flow_config(config, PythonVersion((3, 12))) == own


def test_in_order_past_the_limits():
    """Requests the model cannot take get their statements in order by default, or None with fallback=False."""
    model = tiny_model()
    model.config.max_stmts = 0
    row = {"input": "| <s0> K_cond POP_JUMP_IF_FALSE f+ <s2> | <s1> K_stmt | <s2> K_stmt RETURN_CONST nf", "shapes": "cond stmt stmt", "version": "3.12", "n_stmts": 3, "target": "<s0> { <s1> } <s2>", "loops": []}
    request = CflowRequest.from_row(row)
    straight = CflowRequest.from_row({"input": "| <s0> K_stmt | <s1> K_stmt RETURN_CONST nf", "shapes": "stmt stmt", "version": "3.12"})
    grammar = request.grammar()
    predictor = TransitionPredictor(model)
    assert predictor([request, None], num_beams=2) == [[grammar.complete(grammar.start())], None]
    assert predictor([request, straight, None], num_beams=2, fallback=False) == [None, [["<s0>", "<s1>"]], None]

    sys.path.insert(0, str(Path(__file__).parents[1] / "dev_scripts" / "control_flow"))
    from train_transition import collate, exact_match

    report = exact_match(predictor, [row])
    assert report["predicted"] == 0.0 and report["exact_match"] == 0.0

    # collate honors row["loops"] so LOOP is masked out when loops is empty
    ids, refs, stmt_pos = (
        [model.vocab.get(t, 1) if not t.startswith("<s") else 2 for t in row["input"].split()],
        [int(t[2:-1]) if t.startswith("<s") else -1 for t in row["input"].split()],
        [1, 6, 9],
    )
    batch = collate([row | {"input_ids": ids, "refs": refs, "stmt_pos": stmt_pos, "length": len(ids)}])
    loop_col = batch["allowed"].shape[-1] - len(TOKENS) + TOKENS.index("loop")
    assert not batch["allowed"][0, 0, loop_col]


def test_budget_batches():
    """Every row is in one batch of each epoch, batches keep to the budget, and epochs differ."""
    sys.path.insert(0, str(Path(__file__).parents[1] / "dev_scripts" / "control_flow"))
    from train_transition import BudgetBatches

    rng = np.random.default_rng(0)
    n_stmts = rng.integers(1, 40, 2000)
    n_stmts[:5] = 2000  # a few huge code objects
    rows = {"n_stmts": n_stmts, "length": 4 * n_stmts, "steps": 3 * n_stmts}
    sampler = BudgetBatches(rows, rows=16, shuffle=True, seed=0)
    epochs = [list(sampler) for _ in range(2)]
    for batches in epochs:
        assert sorted(i for b in batches for i in b) == list(range(2000))
        assert abs(len(batches) - len(sampler)) <= len(sampler) // 10
        for b in batches:
            assert len(b) <= 16
            if len(b) > 1:
                assert len(b) * max(rows["length"][b]) <= 16 * BudgetBatches.TOKENS_PER_ROW
                assert len(b) * max(n_stmts[b]) * max(rows["steps"][b]) <= 16 * BudgetBatches.CELLS_PER_ROW
    assert epochs[0] != epochs[1]
    assert [b for b in BudgetBatches(rows, rows=16, shuffle=True, seed=0)] == epochs[0]
