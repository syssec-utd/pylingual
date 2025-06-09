def handle_message(self, msg):
    """Manage message of different type and in the context of path."""
    self.messages.append({'type': msg.category, 'module': msg.module, 'obj': msg.obj, 'line': msg.line, 'column': msg.column, 'path': msg.path, 'symbol': msg.symbol, 'message': html.escape(msg.msg or '', quote=False), 'message-id': msg.msg_id})