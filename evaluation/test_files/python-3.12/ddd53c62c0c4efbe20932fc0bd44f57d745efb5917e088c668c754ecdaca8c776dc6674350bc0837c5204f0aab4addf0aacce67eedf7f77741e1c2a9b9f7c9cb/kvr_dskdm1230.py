import json, requests, hashlib, os, time, redis, fastapi, uvicorn, random, asyncio, platform, spacy, traceback
from collections import Counter
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse, RedirectResponse
app = globals().get('app', fastapi.FastAPI())
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
if not hasattr(redis, 'r'):
    redis.r = redis.Redis(host=os.getenv('rhost', '172.17.0.1' if not 'Windows' in platform.system() else '110.40.247.167'), port=int(os.getenv('rport', 6666)), db=int(os.getenv('rdb', 0)), decode_responses=True)
final_version = lambda rid='2696701': [(k.split('-')[-1], redis.r.zrevrange(k, 0, 0)[0].split(':')[0]) for k in redis.r.keys(f'rid:{rid}:ver-score-uid-*')]
first_version = lambda rid='2696701': [(k.split('-')[-1], redis.r.zrange(k, 0, 0)[0].split(':')[0]) for k in redis.r.keys(f'rid:{rid}:ver-score-uid-*')]
nlp = spacy.load('en_core_web_sm')
doc_tok = lambda doc: [{'i': t.i, 'head': t.head.i, 'lex': t.text, 'lem': t.lemma_, 'pos': t.pos_, 'tag': t.tag_, 'dep': t.dep_, 'gpos': t.head.pos_, 'glem': t.head.lemma_} for t in doc]
doc_chunk = lambda doc: [{'lem': doc[sp.end - 1].lemma_, 'start': sp.start, 'end': sp.end, 'pos': 'NP', 'chunk': sp.text} for sp in doc.noun_chunks]
feedback = lambda arr: [{'cate': v.get('cate', ''), 'topcate': v.get('cate', '').split('.')[0][2:], 'ibeg': v.get('ibeg', -1), 'kp': v.get('kp', ''), 'msg': v.get('short_msg', '')} for k, v in arr.items() if v.get('cate', '').startswith(('e_', 'w_'))]

@app.post('/dskdm/newdsk')
def submit_hdsk(dsk: dict):
    """ NOT tested yet, added 2022.11.30 """
    try:
        info = dsk.get('info', {})
        eid = int(info.get('essay_id', 0))
        ver = str(info.get('e_version', ''))
        eidv = f'{eid}-{ver}'
        if not eid or not ver:
            return f'invaid eid/ver'
        rid = info.get('rid', 0)
        uid = info.get('uid', 0)
        score = info.get('final_score', 0)
        ct = int(info.get('ct', 0))
        snts = [arrsnt['meta'].get('snt', '').strip() for arrsnt in dsk['snt']]
        redis.r.hset(f'rid:{rid}:uid-{uid}:{ver}', 'score', score, {'ver': ver, 'eid': eid, 'rid': rid, 'uid': uid, 'ct': ct, 'snts': json.dumps(snts), 'doc': json.dumps(dsk.get('doc', {})), 'info': json.dumps(info), 'pids': json.dumps([arrsnt['meta'].get('pid', -1) for arrsnt in dsk['snt']])})
        redis.r.expire(f'rid:{rid}:uid-{uid}:{ver}', 3600 * 24 * 180)
        redis.r.zadd(f'rid:{rid}:ver-score-uid-{uid}', {f'{ver}:{score}': ver})
        redis.r.hset(f'uid:{uid}', f'rid:{rid}', score)
        for mkf in dsk['snt']:
            snt = mkf['meta'].get('snt', '').strip()
            if snt and (not redis.r.hexists(f'snt:{snt}', 'meta')):
                doc = nlp(snt)
                redis.r.hset(f'snt:{snt}', 'snt', snt, {'meta': json.dumps(mkf.get('meta', {})), 'feedback': json.dumps(feedback(mkf.get('feedback', {}))), 'tok': json.dumps(doc_tok(doc)), 'chunk': json.dumps(doc_chunk(doc))})
                redis.r.expire(f'snt:{snt}', 3600 * 24 * 180)
        return f'successful:{eidv}'
    except Exception as e:
        print('ex:', e, dsk)
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)

@app.get('/')
def home():
    return HTMLResponse(content=f"<h2> dskdm </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>")

@app.get('/dskdm/version')
def dsk_version(rids: str='2552283,2696701', final: bool=True):
    """ rid:1257077:ver-score-uid-23447214 """
    res = []
    for rid in rids.strip().split(','):
        for k in redis.r.keys(f'rid:{rid}:ver-score-uid-*'):
            ver = redis.r.zrevrange(k, 0, 0)[0].split(':')[0] if final else redis.r.zrange(k, 0, 0)[0].split(':')[0]
            uid = k.split('-')[-1]
            arr = redis.r.hgetall(f'rid:{rid}:uid-{uid}:{ver}')
            arr.update({'rid': rid, 'uid': uid, 'ver': ver, 'final': final})
            res.append(arr)
    return res

@app.get('/dskdm/dims')
def dsk_dims(rids: str='2552283,2696701', final: bool=True, dims: str='awl,ast'):
    """ verbose version of dsk_version, for super large data, 2022.12.29 """
    dims = dims.strip().split(',')
    res = []
    for rid in rids.strip().split(','):
        for k in redis.r.keys(f'rid:{rid}:ver-score-uid-*'):
            ver = redis.r.zrevrange(k, 0, 0)[0].split(':')[0] if final else redis.r.zrange(k, 0, 0)[0].split(':')[0]
            uid = k.split('-')[-1]
            sdoc = redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'doc')
            if sdoc is None:
                continue
            arr = json.loads(sdoc)
            row = {dim: arr[dim] for dim in dims if dim in arr}
            eid = redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'eid')
            row.update({'rid': rid, 'uid': uid, 'ver': ver, 'eid': eid})
            res.append(row)
    return res

@app.get('/dskdm/info')
def dsk_info(rids: str='2552283,2696701', final: bool=True, dims: str='formular_score,final_score'):
    """ get dskdm from info , 2022.12.30 """
    dims = dims.strip().split(',')
    res = []
    for rid in rids.strip().split(','):
        for k in redis.r.keys(f'rid:{rid}:ver-score-uid-*'):
            ver = redis.r.zrevrange(k, 0, 0)[0].split(':')[0] if final else redis.r.zrange(k, 0, 0)[0].split(':')[0]
            uid = k.split('-')[-1]
            sdoc = redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'info')
            if sdoc is None:
                continue
            arr = json.loads(sdoc)
            row = {dim: arr[dim] for dim in dims if dim in arr}
            eid = redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'eid')
            row.update({'rid': rid, 'uid': uid, 'ver': ver, 'eid': eid})
            res.append(row)
    return res

@app.get('/dskdm/version_count')
def dsk_version_count(rids: str='2552283,2696701'):
    """  """
    return [{'rid': rid, 'uid': k.split('-')[-1], 'count': redis.r.zcard(k)} for rid in rids.strip().split(',') for k in redis.r.keys(f'rid:{rid}:ver-score-uid-*')]

@app.get('/dskdm/hgetall')
def dsk_hgetall(key: str='cate', keyname: str='key', valname: str='value'):
    """  """
    return [{keyname: k, valname: v} for k, v in redis.r.hgetall(key).items()]

@app.get('/dskdm/snt')
def dsk_snt(rids: str='2552283,2696701', field: str='tok', final: bool=True):
    """ grafana: extract fields """
    res = []
    for rid in rids.strip().split(','):
        uid_ver = final_version(rid) if final else first_version(rid)
        for uid, ver in uid_ver:
            for snt in json.loads(redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'snts')):
                v = redis.r.hget(f'snt:{snt}', field)
                if field in ('tok', 'feedback', 'chunk'):
                    [res.append({'rid': rid, 'uid': uid, 'snt': snt, field: json.dumps(ar)}) for ar in json.loads(v)]
                else:
                    res.append({'rid': rid, 'uid': uid, 'snt': snt, field: v})
    return res

@app.get('/dskdm/lempos')
def dsk_lempos(rids: str='2552283,2696701', pos: str='VERB', final: bool=True, topk: int=10):
    """ verbose version of dsk_snt, for those large data , added 2022.12.28 """
    si = Counter()
    for rid in rids.strip().split(','):
        uid_ver = final_version(rid) if final else first_version(rid)
        for uid, ver in uid_ver:
            for snt in json.loads(redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'snts')):
                v = redis.r.hget(f'snt:{snt}', 'tok')
                if v is None:
                    continue
                for tok in json.loads(v):
                    if tok['pos'] == pos or pos == 'LEX':
                        si.update({tok['lem']: 1})
    return [{'word': s, 'count': i} for s, i in si.most_common(topk)]

@app.get('/dskdm/feedback')
def dsk_feedback(rids: str='2552283,2696701', field: str='topcate', final: bool=True, topk: int=50):
    """ verbose version of dsk_snt, for those large data , added 2022.12.29 """
    si = Counter()
    for rid in rids.strip().split(','):
        uid_ver = final_version(rid) if final else first_version(rid)
        for uid, ver in uid_ver:
            for snt in json.loads(redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'snts')):
                v = redis.r.hget(f'snt:{snt}', 'feedback')
                if v is None:
                    continue
                for item in json.loads(v):
                    si.update({item[field]: 1})
    return [{field: s, 'count': i} for s, i in si.most_common(topk)]

@app.get('/dskdm/cate-in-snt')
def dsk_cate_in_snt(rids: str='2552283,2696701', hkey: str='feedback', field: str='topcate', value: str='snt', topk: int=10):
    """ 2022.11.21 """
    res = []
    for rid in rids.strip().split(','):
        for uid, ver in final_version(rid):
            for snt in json.loads(redis.r.hget(f'rid:{rid}:uid-{uid}:{ver}', 'snts')):
                v = redis.r.hget(f'snt:{snt}', hkey)
                if v:
                    for ar in json.loads(v):
                        if ar.get(field, '') == value:
                            res.append(dict(ar, **{'rid': rid, 'uid': uid, 'ver': ver, 'snt': snt}))
                            break
                if len(res) >= topk:
                    return res
    return res

@app.get('/dskdm/essay')
def dsk_essay(rid: str='2235895', uid: str='30031900', ver: int=2):
    """ rid:2235895:ver-score-uid-30031900 """
    arr = redis.r.hgetall(f'rid:{rid}:uid-{uid}:{ver}')
    snts = json.loads(arr['snts'])
    arr['mkf'] = [redis.r.hgetall(f'snt:{snt}') for snt in snts]
    return arr
if __name__ == '__main__':
    print(dsk_cate_in_snt())
'\n\n@app.get(\'/dskdm/snt\')\ndef dsk_snt(rids:str="2552283,2696701", field:str=\'tok\'):\n\tres = []\n\tfor rid in rids.strip().split(\',\'):\n\t\tfor uid, ver in final_version(rid): \n\t\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\t\tv = redis.r.hget(f"snt:{snt}", field)\n\t\t\t\tif field in ("tok",\'feedback\',\'chunk\'): # [{},{},...]\n\t\t\t\t\t[res.append( {"rid":rid, "uid":uid, "snt":snt, field: json.dumps(ar)} ) for ar in json.loads(v)]\n\t\t\t\telse: \n\t\t\t\t\tres.append( {"rid":rid, "uid":uid, "snt":snt, field: v} )\n\treturn res\n\nfrom collections import Counter\n@app.get(\'/dskdm/tok/si\')\ndef dsk_tok_si(rid:str="2235895", field:str=\'pos\'):\n\t#data for pos chart, field: pos/lex \n\tsi = Counter()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\t[ si.update({t[field]:1}) for t in json.loads(arr[\'tok\']) ]\n\treturn si.most_common()\n\n@app.get(\'/dskdm/cate\')\ndef dsk_cate(rid:str="2235895"):\n\tsi = Counter()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\tfor kp,v  in json.loads(arr[\'feedback\']).items(): \n\t\t\t\tif v[\'cate\'].startswith ( (\'e_\', \'w_\') ): \n\t\t\t\t\tsi.update({v[\'cate\']:1})\n\treturn si.most_common()\n\n@app.get(\'/dskdm/lemma\')\ndef dsk_lemma(rid:str="2696716", pos:str=\'VERB\'):\n\tsi = Counter()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\t[ si.update({t[\'lem\']:1}) for t in json.loads(arr[\'tok\']) if t[\'pos\'] == pos ]\n\treturn si.most_common()\n\n@app.get(\'/dskdm/trp\')\ndef dsk_trp(rid:str="2696716", gpos:str=\'VERB\', pos:str=\'NOUN\', dep:str=\'dobj\'):\n\tsi = Counter()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\t[ si.update({t[\'glem\'] +":"+ t[\'lem\']:1}) for t in json.loads(arr[\'tok\']) if t[\'gpos\'] == gpos and t[\'pos\'] == pos and t[\'dep\'] == dep ]\n\treturn si.most_common()\n\n@app.get(\'/dskdm/cate_in_snt\')\ndef dsk_cate_in_snt(rid:str="2696716", cate:str=\'w_trp.chig\', topk:int=10):\n\tsnts = set()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\tfor kp, v in json.loads(arr[\'feedback\']).items():\n\t\t\t\tif v[\'cate\'] == cate :\n\t\t\t\t\tsnts.add(snt)\n\t\t\t\t\tbreak\n\treturn snts\n\n@app.get(\'/dskdm/lemma_in_snt\')\ndef dsk_lemma_in_snt(rid:str="2696716", pos:str=\'VERB\', lemma:str=\'visit\', topk:int=10):\n\tsnts = set()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\tfor t in json.loads(arr[\'tok\']):\n\t\t\t\tif t[\'pos\'] == pos and t[\'lem\'] == lemma:\n\t\t\t\t\tsnts.add(snt)\n\t\t\t\t\tbreak\n\treturn snts\n\n@app.get(\'/dskdm/trp_in_snt\')\ndef dsk_trp_in_snt(rid:str="2696716", gpos:str=\'VERB\', glem:str=\'visit\', pos:str=\'NOUN\', lem:str=\'parent\', dep:str=\'dobj\'):\n\tsnts = set()\n\tfor uid, ver in final_version(rid): \n\t\tfor snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", \'snts\')):\n\t\t\tarr = redis.r.hgetall(f"snt:{snt}")\n\t\t\tfor t in json.loads(arr[\'tok\']):\n\t\t\t\tif t[\'pos\'] == pos and t[\'lem\'] == lem and t[\'gpos\'] == gpos and t[\'glem\'] == glem and t[\'dep\'] == dep:\n\t\t\t\t\tsnts.add(snt)\n\t\t\t\t\tbreak\n\treturn snts\n'