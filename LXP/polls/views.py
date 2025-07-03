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

        # You would typically retrieve questions again (e.g., from session or cache)
        questions = request.session.get("generated_questions", [])

        selected_questions = [questions[int(idx)] for idx in selected_indexes]

        # TEMP: For debugging or demo, store in session or print
        request.session['selected_polls'] = selected_questions

        # For now, redirect to a success or confirmation page
        return render(request, "trainer/polls/poll_selection_success.html", {
            "selected_questions": selected_questions
        })

    return redirect("trainer-generate-polls")  # fallback if not POST
