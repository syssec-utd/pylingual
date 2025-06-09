from __future__ import annotations
import ast
import asyncio
from enum import Enum
from typing import TYPE_CHECKING, Any, Awaitable, Callable, List, Optional, Type, Union, cast
from ....utils.async_itertools import async_next
from ....utils.logging import LoggingDescriptor
from ....utils.uri import Uri
from ...common.decorators import language_id
from ...common.lsp_types import Location, LocationLink, Position
from ...common.text_document import TextDocument
from ..utils.ast_utils import HasTokens, Token, get_nodes_at_position, get_tokens_at_position, range_from_token
if TYPE_CHECKING:
    from ..protocol import RobotLanguageServerProtocol
from .model_helper import ModelHelperMixin
from .protocol_part import RobotLanguageServerProtocolPart

class CollectType(Enum):
    DEFINITION = 1
    IMPLEMENTATION = 2
_CollectMethod = Callable[[ast.AST, List[ast.AST], TextDocument, Position, CollectType], Awaitable[Union[Location, List[Location], List[LocationLink], None]]]

class RobotGotoProtocolPart(RobotLanguageServerProtocolPart, ModelHelperMixin):
    _logger = LoggingDescriptor()

    def __init__(self, parent: RobotLanguageServerProtocol) -> None:
        super().__init__(parent)
        parent.definition.collect.add(self.collect_definition)
        parent.implementation.collect.add(self.collect_implementation)

    def _find_method(self, cls: Type[Any]) -> Optional[_CollectMethod]:
        if cls is ast.AST:
            return None
        method_name = 'definition_' + cls.__name__
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                return cast(_CollectMethod, method)
        for base in cls.__bases__:
            method = self._find_method(base)
            if method:
                return cast(_CollectMethod, method)
        return None

    @language_id('robotframework')
    @_logger.call
    async def collect_definition(self, sender: Any, document: TextDocument, position: Position) -> Union[Location, List[Location], List[LocationLink], None]:
        return await self.collect(document, position, CollectType.DEFINITION)

    @language_id('robotframework')
    @_logger.call
    async def collect_implementation(self, sender: Any, document: TextDocument, position: Position) -> Union[Location, List[Location], List[LocationLink], None]:
        return await self.collect(document, position, CollectType.IMPLEMENTATION)

    @_logger.call
    async def collect(self, document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        result_nodes = await get_nodes_at_position(await self.parent.documents_cache.get_model(document), position)
        if not result_nodes:
            return None
        result_node = result_nodes[-1]
        if result_node is None:
            return None
        result = await self._definition_default(result_nodes, document, position, collect_type)
        if result:
            return result
        method = self._find_method(type(result_node))
        if method is not None:
            result = await method(result_node, result_nodes, document, position, collect_type)
            if result is not None:
                return result
        return None

    async def _definition_default(self, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        namespace = await self.parent.documents_cache.get_namespace(document)
        if namespace is None:
            return None
        if not nodes:
            return None
        node = nodes[-1]
        if not isinstance(node, HasTokens):
            return None
        tokens = get_tokens_at_position(node, position)
        for token in tokens:
            token_and_var = await async_next(((var_token, var) async for var_token, var in self.iter_variables_from_token(token, namespace, nodes, position, skip_commandline_variables=True) if position in range_from_token(var_token)), None)
            if token_and_var is not None:
                var_token, variable = token_and_var
                if variable.source:
                    return [LocationLink(origin_selection_range=range_from_token(var_token), target_uri=str(Uri.from_path(variable.source)), target_range=variable.range, target_selection_range=range_from_token(variable.name_token) if variable.name_token else variable.range)]
        return None

    async def definition_IfHeader(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import IfHeader
        namespace = await self.parent.documents_cache.get_namespace(document)
        if namespace is None:
            return None
        header = cast(IfHeader, node)
        expression_token = header.get_token(RobotToken.ARGUMENT)
        if expression_token is not None and position in range_from_token(expression_token):
            token_and_var = await async_next(((var_token, var) async for var_token, var in self.iter_expression_variables_from_token(expression_token, namespace, nodes, position, skip_commandline_variables=True) if position in range_from_token(var_token)), None)
            if token_and_var is not None:
                var_token, variable = token_and_var
                if variable.source:
                    return [LocationLink(origin_selection_range=range_from_token(var_token), target_uri=str(Uri.from_path(variable.source)), target_range=variable.range, target_selection_range=range_from_token(variable.name_token) if variable.name_token else variable.range)]
        return None

    async def definition_WhileHeader(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import WhileHeader
        namespace = await self.parent.documents_cache.get_namespace(document)
        if namespace is None:
            return None
        header = cast(WhileHeader, node)
        expression_token = header.get_token(RobotToken.ARGUMENT)
        if expression_token is not None and position in range_from_token(expression_token):
            token_and_var = await async_next(((var_token, var) async for var_token, var in self.iter_expression_variables_from_token(expression_token, namespace, nodes, position, skip_commandline_variables=True) if position in range_from_token(var_token)), None)
            if token_and_var is not None:
                var_token, variable = token_and_var
                if variable.source:
                    return [LocationLink(origin_selection_range=range_from_token(var_token), target_uri=str(Uri.from_path(variable.source)), target_range=variable.range, target_selection_range=range_from_token(variable.name_token) if variable.name_token else variable.range)]
        return None

    async def definition_KeywordName(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import KeywordName
        namespace = await self.parent.documents_cache.get_namespace(document)
        if namespace is None:
            return None
        kw_node = cast(KeywordName, node)
        name_token = cast(RobotToken, kw_node.get_token(RobotToken.KEYWORD_NAME))
        if not name_token:
            return None
        result = await self.get_keyword_definition_at_token(namespace, name_token)
        if result is not None and (not result.is_error_handler) and result.source:
            token_range = range_from_token(name_token)
            return [LocationLink(origin_selection_range=token_range, target_uri=str(Uri.from_path(result.source)), target_range=token_range, target_selection_range=token_range)]
        return None

    async def definition_KeywordCall(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import KeywordCall
        namespace = await self.parent.documents_cache.get_namespace(document)
        if namespace is None:
            return None
        kw_node = cast(KeywordCall, node)
        result = await self.get_keyworddoc_and_token_from_position(kw_node.keyword, cast(Token, kw_node.get_token(RobotToken.KEYWORD)), [cast(Token, t) for t in kw_node.get_tokens(RobotToken.ARGUMENT)], namespace, position)
        if result is not None:
            keyword_doc, keyword_token = result
            if await namespace.find_keyword(keyword_token.value, raise_keyword_error=False, handle_bdd_style=False) is None:
                keyword_token = self.strip_bdd_prefix(namespace, keyword_token)
            lib_entry, kw_namespace = await self.get_namespace_info_from_keyword(namespace, keyword_token)
            kw_range = range_from_token(keyword_token)
            if lib_entry and kw_namespace:
                r = range_from_token(keyword_token)
                r.end.character = r.start.character + len(kw_namespace)
                kw_range.start.character = r.end.character + 1
                if position in r:
                    if collect_type == CollectType.DEFINITION and lib_entry.import_source:
                        return [LocationLink(origin_selection_range=r, target_uri=str(Uri.from_path(lib_entry.import_source)), target_range=lib_entry.import_range, target_selection_range=lib_entry.import_range)]
                    if lib_entry.library_doc and lib_entry.library_doc.source_or_origin:
                        return [LocationLink(origin_selection_range=r, target_uri=str(Uri.from_path(lib_entry.library_doc.source_or_origin)), target_range=lib_entry.import_range, target_selection_range=lib_entry.import_range)]
                    else:
                        return None
            if position in kw_range and keyword_doc is not None and keyword_doc.source:
                return [LocationLink(origin_selection_range=kw_range, target_uri=str(Uri.from_path(keyword_doc.source)), target_range=keyword_doc.range, target_selection_range=keyword_doc.range)]
        return None

    async def definition_Fixture(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import Fixture
        namespace = await self.parent.documents_cache.get_namespace(document)
        if namespace is None:
            return None
        fixture_node = cast(Fixture, node)
        name_token = cast(Token, fixture_node.get_token(RobotToken.NAME))
        if name_token is None or name_token.value is None or name_token.value.upper() in ('', 'NONE'):
            return None
        result = await self.get_keyworddoc_and_token_from_position(fixture_node.name, name_token, [cast(Token, t) for t in fixture_node.get_tokens(RobotToken.ARGUMENT)], namespace, position)
        if result is not None:
            keyword_doc, keyword_token = result
            if await namespace.find_keyword(keyword_token.value, raise_keyword_error=False, handle_bdd_style=False) is None:
                keyword_token = self.strip_bdd_prefix(namespace, keyword_token)
            lib_entry, kw_namespace = await self.get_namespace_info_from_keyword(namespace, keyword_token)
            kw_range = range_from_token(keyword_token)
            if lib_entry and kw_namespace:
                r = range_from_token(keyword_token)
                r.end.character = r.start.character + len(kw_namespace)
                kw_range.start.character = r.end.character + 1
                if position in r:
                    if collect_type == CollectType.DEFINITION and lib_entry.import_source:
                        return [LocationLink(origin_selection_range=r, target_uri=str(Uri.from_path(lib_entry.import_source)), target_range=lib_entry.import_range, target_selection_range=lib_entry.import_range)]
                    if lib_entry.library_doc and lib_entry.library_doc.source_or_origin:
                        return [LocationLink(origin_selection_range=r, target_uri=str(Uri.from_path(lib_entry.library_doc.source_or_origin)), target_range=lib_entry.import_range, target_selection_range=lib_entry.import_range)]
                    else:
                        return None
            if position in kw_range and keyword_doc is not None and keyword_doc.source:
                return [LocationLink(origin_selection_range=kw_range, target_uri=str(Uri.from_path(keyword_doc.source)), target_range=keyword_doc.range, target_selection_range=keyword_doc.range)]
        return None

    async def _definition_Template_or_TestTemplate(self, template_node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import Template, TestTemplate
        template_node = cast(Union[Template, TestTemplate], template_node)
        if template_node.value:
            keyword_token = cast(RobotToken, template_node.get_token(RobotToken.NAME))
            if keyword_token is None or keyword_token.value is None or keyword_token.value.upper() in ('', 'NONE'):
                return None
            namespace = await self.parent.documents_cache.get_namespace(document)
            if namespace is None:
                return None
            if await namespace.find_keyword(keyword_token.value, raise_keyword_error=False, handle_bdd_style=False) is None:
                keyword_token = self.strip_bdd_prefix(namespace, keyword_token)
            if position.is_in_range(range_from_token(keyword_token)):
                keyword_doc = await namespace.find_keyword(template_node.value)
                if keyword_doc is not None:
                    lib_entry, kw_namespace = await self.get_namespace_info_from_keyword(namespace, keyword_token)
                    kw_range = range_from_token(keyword_token)
                    if lib_entry and kw_namespace:
                        r = range_from_token(keyword_token)
                        r.end.character = r.start.character + len(kw_namespace)
                        kw_range.start.character = r.end.character + 1
                        if position in r:
                            if collect_type == CollectType.DEFINITION and lib_entry.import_source:
                                return [LocationLink(origin_selection_range=r, target_uri=str(Uri.from_path(lib_entry.import_source)), target_range=lib_entry.import_range, target_selection_range=lib_entry.import_range)]
                            if lib_entry.library_doc and lib_entry.library_doc.source_or_origin:
                                return [LocationLink(origin_selection_range=r, target_uri=str(Uri.from_path(lib_entry.library_doc.source_or_origin)), target_range=lib_entry.import_range, target_selection_range=lib_entry.import_range)]
                            else:
                                return None
                    if keyword_doc.source and (not keyword_doc.is_error_handler):
                        return [LocationLink(origin_selection_range=kw_range, target_uri=str(Uri.from_path(keyword_doc.source)), target_range=keyword_doc.range, target_selection_range=keyword_doc.range)]
        return None

    async def definition_TestTemplate(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        return await self._definition_Template_or_TestTemplate(node, nodes, document, position, collect_type)

    async def definition_Template(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        return await self._definition_Template_or_TestTemplate(node, nodes, document, position, collect_type)

    async def definition_LibraryImport(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import LibraryImport
        library_node = cast(LibraryImport, node)
        if library_node.name:
            name_token = cast(RobotToken, library_node.get_token(RobotToken.NAME))
            if name_token is None:
                return None
            if position.is_in_range(range_from_token(name_token)):
                namespace = await self.parent.documents_cache.get_namespace(document)
                if namespace is None:
                    return None
                try:
                    libdoc = await namespace.get_imported_library_libdoc(library_node.name, library_node.args, library_node.alias)
                    if libdoc is None or libdoc.errors:
                        libdoc = await namespace.imports_manager.get_libdoc_for_library_import(str(library_node.name), (), str(document.uri.to_path().parent), variables=await namespace.get_resolvable_variables())
                    if libdoc is None:
                        return None
                    python_source = libdoc.source_or_origin
                    if python_source is not None:
                        return [LocationLink(origin_selection_range=range_from_token(name_token), target_uri=str(Uri.from_path(python_source)), target_range=libdoc.range, target_selection_range=libdoc.range)]
                except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                    raise
                except BaseException:
                    pass
        return None

    async def definition_ResourceImport(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import ResourceImport
        resource_node = cast(ResourceImport, node)
        if resource_node.name:
            name_token = cast(RobotToken, resource_node.get_token(RobotToken.NAME))
            if name_token is None:
                return None
            if position.is_in_range(range_from_token(name_token)):
                namespace = await self.parent.documents_cache.get_namespace(document)
                if namespace is None:
                    return None
                try:
                    libdoc = await namespace.get_imported_resource_libdoc(resource_node.name)
                    if libdoc is None or libdoc.errors:
                        libdoc = await namespace.imports_manager.get_libdoc_for_resource_import(str(resource_node.name), str(document.uri.to_path().parent), variables=await namespace.get_resolvable_variables())
                    if libdoc is None:
                        return None
                    python_source = libdoc.source_or_origin
                    if python_source is not None:
                        return [LocationLink(origin_selection_range=range_from_token(name_token), target_uri=str(Uri.from_path(python_source)), target_range=libdoc.range, target_selection_range=libdoc.range)]
                except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                    raise
                except BaseException:
                    pass
        return None

    async def definition_VariablesImport(self, node: ast.AST, nodes: List[ast.AST], document: TextDocument, position: Position, collect_type: CollectType) -> Union[Location, List[Location], List[LocationLink], None]:
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import VariablesImport
        variables_node = cast(VariablesImport, node)
        if variables_node.name:
            name_token = cast(RobotToken, variables_node.get_token(RobotToken.NAME))
            if name_token is None:
                return None
            if position.is_in_range(range_from_token(name_token)):
                namespace = await self.parent.documents_cache.get_namespace(document)
                if namespace is None:
                    return None
                try:
                    libdoc = await namespace.get_imported_variables_libdoc(variables_node.name, variables_node.args)
                    if libdoc is None or libdoc.errors:
                        libdoc = await namespace.imports_manager.get_libdoc_for_variables_import(str(variables_node.name), (), str(document.uri.to_path().parent), variables=await namespace.get_resolvable_variables())
                    if libdoc is None:
                        return None
                    python_source = libdoc.source_or_origin
                    if python_source is not None:
                        return [LocationLink(origin_selection_range=range_from_token(name_token), target_uri=str(Uri.from_path(python_source)), target_range=libdoc.range, target_selection_range=libdoc.range)]
                except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                    raise
                except BaseException:
                    pass
        return None