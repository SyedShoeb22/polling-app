# polls/views.py
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PollGenerateForm
from .models import Poll, PollOption
from .services import fetch_mcqs
from django.contrib.auth.decorators import login_required
from polls.ai_helpers.question_generator import build_prompt, ask_openrouter, parse_mcqs
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import PollGenerateForm
from .fastapi_runner import start_fastapi  # import this
from polls.models import Question  # adjust 'polls' based on your app name

_fastapi_started = False
def ensure_fastapi_running():
    global _fastapi_started
    if not _fastapi_started:
        start_fastapi()
        _fastapi_started = True

def trainer_generate_polls(request):
    ensure_fastapi_running() 
    form = PollGenerateForm(request.POST or None)
    questions = []

    if request.method == "POST" and form.is_valid():
        topics = form.cleaned_data["topics"]
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(",")]
        
        n_questions = form.cleaned_data["n_questions"]
        questions = fetch_mcqs(topics, n_questions)
        request.session["generated_questions"] = questions

    return render(request, "trainer/polls/trainer_generate_polls.html", {
        "form": form,
        "questions": questions
    })


def save_selected_polls(request):
    if request.method == "POST":
        selected_indexes = request.POST.getlist("selected_questions")
        generated_questions = request.session.get("generated_questions", [])
        
        user = request.user if request.user.is_authenticated else None  # 🟢 Add this line here

        # ✅ Create the Poll (you can let user give a name, here hardcoded for demo)
        poll = Poll.objects.create(
            title="AI Generated Poll",
            created_by=user,
        )

        # ✅ Create Questions under that Poll
        for i in selected_indexes:
            try:
                q = generated_questions[int(i)]
                Question.objects.create(
                    poll=poll,
                    question=q["question"],
                    options=q["options"],
                    answer_index=q["answer_index"],
                )
            except (IndexError, KeyError, ValueError) as e:
                print("Skipping malformed question:", e)
                continue

        # Redirect to poll list/detail etc.
        return redirect("poll_detail", poll_id=poll.id)

    return redirect("trainer_generate_polls")

from django.shortcuts import render, get_object_or_404
from .models import Poll

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, "trainer/polls/poll_detail.html", {"poll": poll})
