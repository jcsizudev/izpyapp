from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
  name = '誰なんだか'
  return render_template('hello.html', title='Flask test', name=name)

if __name__ == '__main__':
  app.run()
