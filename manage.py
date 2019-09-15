from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User,Question

manager = Manager(app)

# 使用migrate 绑定 app 和 db
migrate = Migrate(app, db)

# 添加迁移版本的命令到 migrate 中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()