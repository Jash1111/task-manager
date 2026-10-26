from flask import Flask, redirect, render_template_string, request, url_for
#test webhook
app = Flask(__name__)

APP_VERSION = "v4"
tasks = []  # in-memory store, kept simple on purpose

PAGE = """
<!doctype html>
<html>
<head>
  <title>Task Manager</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; }
    li { margin: 8px 0; }
    .ver { color: #667085; font-size: 14px; }
  </style>
</head>
<body>
  <h1>Task Manager <span class="ver">{{ version }}</span></h1>
  <form method="post" action="/add">
    <input name="title" placeholder="New task" required>
    <button type="submit">Add</button>
  </form>
  <ul>
    {% for t in tasks %}
      <li>{{ t.title }} <a href="/delete/{{ t.id }}">delete</a></li>
    {% else %}
      <li>No tasks yet.</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE, tasks=tasks, version=APP_VERSION)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        next_id = max((t["id"] for t in tasks), default=0) + 1
        tasks.append({"id": next_id, "title": title})
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks[:] = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
