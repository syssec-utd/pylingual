def run_cell(self, raw_cell, store_history=False, silent=False):
    """Run a complete IPython cell.

        Parameters
        ----------
        raw_cell : str
          The code (including IPython code such as %magic functions) to run.
        store_history : bool
          If True, the raw and translated cell will be stored in IPython's
          history. For user code calling back into IPython's machinery, this
          should be set to False.
        silent : bool
          If True, avoid side-effets, such as implicit displayhooks, history,
          and logging.  silent=True forces store_history=False.
        """
    if not raw_cell or raw_cell.isspace():
        return
    if silent:
        store_history = False
    self.input_splitter.push(raw_cell)
    if self.input_splitter.cell_magic_parts:
        self._current_cell_magic_body = ''.join(self.input_splitter.cell_magic_parts)
    cell = self.input_splitter.source_reset()
    with self.builtin_trap:
        prefilter_failed = False
        if len(cell.splitlines()) == 1:
            try:
                cell = self.prefilter_manager.prefilter_lines(cell) + '\n'
            except AliasError as e:
                error(e)
                prefilter_failed = True
            except Exception:
                self.showtraceback()
                prefilter_failed = True
        if store_history:
            self.history_manager.store_inputs(self.execution_count, cell, raw_cell)
        if not silent:
            self.logger.log(cell, raw_cell)
        if not prefilter_failed:
            cell_name = self.compile.cache(cell, self.execution_count)
            with self.display_trap:
                try:
                    code_ast = self.compile.ast_parse(cell, filename=cell_name)
                except IndentationError:
                    self.showindentationerror()
                    if store_history:
                        self.execution_count += 1
                    return None
                except (OverflowError, SyntaxError, ValueError, TypeError, MemoryError):
                    self.showsyntaxerror()
                    if store_history:
                        self.execution_count += 1
                    return None
                interactivity = 'none' if silent else self.ast_node_interactivity
                self.run_ast_nodes(code_ast.body, cell_name, interactivity=interactivity)
                post_exec = [] if silent else self._post_execute.iteritems()
                for func, status in post_exec:
                    if self.disable_failing_post_execute and (not status):
                        continue
                    try:
                        func()
                    except KeyboardInterrupt:
                        (print >> io.stderr, '\nKeyboardInterrupt')
                    except Exception:
                        self._post_execute[func] = False
                        self.showtraceback()
                        (print >> io.stderr, '\n'.join(['post-execution function %r produced an error.' % func, 'If this problem persists, you can disable failing post-exec functions with:', '', '    get_ipython().disable_failing_post_execute = True']))
    if store_history:
        self.history_manager.store_output(self.execution_count)
        self.execution_count += 1