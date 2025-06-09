import re
from importlib.metadata import version
from typing import Optional, Callable, Any
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from termcolor import colored, cprint
from ltou.model import Context, MenuEntry, SingularMenuModel, MultiselectMenuModel, BaseMenuModel, DatabaseDSN, SKIP_ENTRY
from click import Command, Option

class SnakeCaseValidator(Validator):
    snake_case_regex = re.compile('^(?!_)(?!.*__)[a-z]+(_[a-z]+)*$')

    def validate(self, document):
        text = document.text
        if not text and re.fullmatch(self.snake_case_regex, text) is None:
            raise ValidationError(message=f'Invalid snake_case: {text}')

def db_menu_update_info(ctx: Context, menu: SingularMenuModel) -> Context:
    for entry in menu.entries:
        if entry.code == ctx.db:
            ctx.db_info = entry.additional_info.dict()
    return ctx

def disable_orm(ctx: Context) -> MenuEntry:
    if ctx.db == 'none':
        ctx.orm = 'none'
        return SKIP_ENTRY
    return ctx.db
db_menu = SingularMenuModel(title='❯ Choose your database: 🐥', code='db', description='Select a database for your app', after_ask_fun=db_menu_update_info, entries=[MenuEntry(code='none', user_view='No database', description="This project doesn't need a database.", additional_info=DatabaseDSN(name='none', image=None, driver=None, async_driver=None, port=None)), MenuEntry(code='postgresql', user_view='PostgreSQL', description="{name}[Network] is second most popular open-source relational database.\nIt's a good fit for {prod} application.".format(name=colored('PostgreSQL', color='green'), prod=colored('production-grade', color='cyan', attrs=['underline'])), additional_info=DatabaseDSN(name='postgresql', image='postgres:15.2-alpine', async_driver='postgresql+asyncpg', driver_short='postgres', driver='postgresql', port=5432), available_orm=['none', 'sqlmodel', 'sa2']), MenuEntry(code='mongodb', user_view='MongoDB', description="{name} is a non-relational document database that provides support for JSON-like storage.\nIt's a good fit for {prod} application.".format(name=colored('Mongodb', color='green'), prod=colored('MongoDB 6.0', color='cyan', attrs=['underline'])), additional_info=DatabaseDSN(name='mongodb', image='mongo', driver_short='mongodb', driver='mongodb', port=27017), available_orm=['none', 'beanie', 'mongo']), MenuEntry(code='sqlite', user_view='SQLite', description='{name} SQLite[Memory] is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured,.\nThis option will be a great fit for {small} systems where you are going to run {how_many} of your application.'.format(name=colored('SQLite', color='green'), small=colored('small', color='cyan', attrs=['underline']), how_many=colored('only one instance', color='red', attrs=['bold', 'underline'])), additional_info=DatabaseDSN(name='sqlite', image=None, async_driver='sqlite+aiosqlite', driver_short='sqlite', driver='sqlite', port=None), available_orm=['none', 'sqlmodel', 'sa2']), MenuEntry(code='mysql', user_view='MySQL', description="{name}[Network] is the most popular database made by oracle.\nIt's a good fit for {prod} application.".format(name=colored('MySQL', color='green'), prod=colored('production-grade', color='cyan', attrs=['underline'])), additional_info=DatabaseDSN(name='mysql', image='bitnami/mysql', async_driver='mysql+aiomysql', driver_short='mysql', driver='mysql', port=3306), available_orm=['none', 'sqlmodel', 'sa2'])])
orm_menu = SingularMenuModel(title='❯ Choose your database ORM: ', code='orm', description='Choose Object–Relational Mapper lib', cli_name='orm', before_ask_fun=disable_orm, entries=[MenuEntry(code='none', user_view='Without ORMs', description='If you select this option, you will get only {what}.\nThe rest {warn}.'.format(what=colored('raw database', color='green'), warn=colored('is up to you', color='red', attrs=['underline']))), MenuEntry(code='sqlmodel', user_view='SQLModel', description="{what} is a great {feature} ORM. only support SQLAlchemy1.x \nIt's compatible with pydantic models and move_alembic migrator.".format(what=colored('Ormar', color='green'), feature=colored('SQLAlchemy1.0', color='cyan')), aavailable_orm=['sqlite', 'postgresql', 'mysql']), MenuEntry(code='sa2', user_view='SQLAlchemy 2.0', description='{what} is the most popular python ORM.\nIt has a {feature} and a big community around it.'.format(what=colored('SQLAlchemy2.0', color='green'), feature=colored('The SQLAlchemy SQL Toolkit', color='cyan')), available_orm=['sqlite', 'postgresql', 'mysql']), MenuEntry(code='beanie', user_view='Beanie', description='{what} is an Asynchronous Python ODM for MongoDB.\nIt has a {feature} and a big community around it.'.format(what=colored('Beanie', color='green'), feature=colored('Beanie', color='cyan')), available_orm=['mongodb']), MenuEntry(code='tortoise', user_view='Tortoise', description='{what} ORM is an easy-to-use asyncio SQL ORM.\nIt has a {feature} and a big community around it.'.format(what=colored('Tortoise', color='green'), feature=colored('Tortoise', color='cyan')), available_orm=['sqlite', 'postgresql', 'mysql']), MenuEntry(code='mongo', user_view='PyMongo', description='{what} is a popular NoSQL database.\nuses JSON-like documents with optional schemas.'.format(what=colored('PyMongo[Motor]', color='green'), feature=colored('PyMongo[Motor]', color='cyan')), available_orm=['mongodb'])])

def do_not_ask_features_if_quite(ctx: Context) -> Optional[list[MenuEntry]]:
    if ctx.quite:
        return [SKIP_ENTRY]
    return None
features_menu = MultiselectMenuModel(title='❯ Choose your preset features: ', code='features', description='Additional project features', multiselect=True, before_ask=do_not_ask_features_if_quite, entries=[MenuEntry(code='enable_celery', cli_name='celery', user_view='Add Celery support', description="{name} is a flexible message broker.\nIt's used to create {purp1} systems or for {purp2}.".format(name=colored('Celery', color='green'), purp1=colored('event-based', color='cyan'), purp2=colored('async computations', color='cyan'))), MenuEntry(code='enable_sentry', cli_name='sentry', user_view='Add sentry integration', description='{what} is super cool system that helps finding bugs.\nThis feature will add sentry integration to your project. ({warn}).'.format(what=colored('Sentry', color='green'), warn=colored('This option may decrease speed', color='red', attrs=['underline']))), MenuEntry(code='enable_redis', cli_name='redis', user_view='Add redis support', description="{name} is a cool and lightweight in-memory key-value store.\nIt's good for {purpose1} or {purpose2}.".format(name=colored('Redis', color='green'), purpose1=colored('caching', color='cyan'), purpose2=colored('storing temporary variables', color='cyan'))), MenuEntry(code='enable_rmq', cli_name='rabbit', user_view='Add RabbitMQ support', description="{name} is a flexible message broker.\nIt's used to create {purp1} systems or for {purp2}.".format(name=colored('RabbitMQ', color='green'), purp1=colored('event-based', color='cyan'), purp2=colored('async computations', color='cyan'))), MenuEntry(code='enable_kafka', cli_name='kafka', user_view='Add Kafka support', description="{what} is a message broker.\nKafka doesn't have a fancy routing as RabbitMQ, but it's {why}.".format(what=colored('Kafka', color='green'), why=colored('super fast', color='cyan'))), MenuEntry(code='enable_loguru', cli_name='Loguru', user_view='Add Loguru logger', description='{what} is a library which aims to bring enjoyable logging.\nLoguru tries to make it both . support asynchronous'.format(what=colored('Loguru', color='green'), why=colored('pleasant and powerful', color='cyan', attrs=['underline'])))])
ci_menu = SingularMenuModel(title='❯ Choose your CI|CD: ', code='ci_type', cli_name='ci', description='Select a CI for your app', entries=[MenuEntry(code='none', user_view='Do not add CI/CD.', description="This project doesn't need to have CI/CD."), MenuEntry(code='gitlab_ci', user_view='Gitlab CI', description='Use this option if you use gitlab as your VCS.\nThis option will add test jobs in your {file} file.\n({warn}).'.format(file=colored('`.gitlab-ci.yml`', color='cyan'), warn=colored('the GitLab built-in Continuous Integration', color='red', attrs=['underline']))), MenuEntry(code='github', user_view='Github Actions', description='Use this option if you use github as your VCS.\nThis option will create {file} file that adds test jobs for your project.'.format(file=colored('`.github/workflows/tests.yml`', color='cyan'))), MenuEntry(code='jenkins', user_view='Jenkins', description='Use this option if you automate their build, test and release workflows \nThis option will create {file} yaml for your project.'.format(file=colored('`.jenkins.yaml`', color='cyan'))), MenuEntry(code='drone', user_view='Drone CI', description='Use this option if you automate their build, test and release workflows .\nThis option will create {file} yaml for your project.'.format(file=colored('`.drone.yaml`', color='cyan')))])

def handle_cli(menus: list[BaseMenuModel], callback: Callable[[Context], None]):

    def inner_callback(**cli_args: Any):
        if cli_args['version']:
            print(version('ltou'))
            exit(0)
        context = Context(**cli_args)
        if context.project_name is None:
            context.project_name = prompt('❯ Project name: ', validator=SnakeCaseValidator())
        context.project_name = context.project_name.strip()
        for menu in menus:
            if menu.need_ask(context):
                context = menu.ask(context)
                if context is None:
                    print('Project generation stopped. Goodbye!')
                    return
                context = Context(**context.dict())
            context = Context(**menu.after_ask(context=context).dict())
        callback(context)
    return inner_callback

def run_command(callback: Callable[[Context], None]) -> None:
    menus: 'list[BaseMenuModel]' = [db_menu, orm_menu, features_menu, ci_menu]
    cmd = Command(None, params=[Option(['-n', '--new', 'project_name'], help='Create a new project'), Option(['-V', '--version', 'version'], is_flag=True, help='Prints current version'), Option(['--force'], is_flag=True, help='Overwrite directory if it exists'), Option(['--quite'], is_flag=True, help='Do not ask for features during generation')], callback=handle_cli(menus=menus, callback=callback))
    for menu in menus:
        cmd.params.extend(menu.get_cli_options())
    cmd.main()
if __name__ == '__main__':
    run_command()