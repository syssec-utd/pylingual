def get_ast(self, filepath, modname):
    """return an ast(roid) representation for a module"""
    try:
        return MANAGER.ast_from_file(filepath, modname, source=True)
    except astroid.AstroidSyntaxError as ex:
        self.add_message('syntax-error', line=getattr(ex.error, 'lineno', 0), args=str(ex.error))
    except astroid.AstroidBuildingException as ex:
        self.add_message('parse-error', args=ex)
    except Exception as ex:
        import traceback
        traceback.print_exc()
        self.add_message('astroid-error', args=(ex.__class__, ex))