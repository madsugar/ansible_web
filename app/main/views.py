from . import main


@main.route('/test', methods=['GET', 'POST'])
def test():
    return "test, this is my test"
