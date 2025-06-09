from fastapi import APIRouter, Request
from pydantic import BaseModel
from yyxx_game_pkg.xtrace.helper import get_current_trace_id, add_span_tags, add_span_events
router = APIRouter()

class Message(BaseModel):
    content: dict

@router.post('/submit')
async def submit(request: Request, msg: Message):
    from yyxx_game_pkg.stat.dispatch.logic.task_logic import task_logic
    add_span_events('schedule', {'content': str(msg.content)})
    add_span_tags(msg.content)
    trace_id = get_current_trace_id()
    task_id_list = task_logic(msg.content)
    add_span_events('results', {'task_id_list': str(task_id_list)})
    return {'task_id_list': task_id_list, 'trace_id': trace_id}