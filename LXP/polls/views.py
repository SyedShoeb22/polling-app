# polls/views.py
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PollGenerateForm
from .models import Poll, PollOption
from .services import fetch_mcqs
from django.contrib.auth.decorators import login_required
from polls.ai_helpers.question_generator import build_prompt, ask_openrouter, parse_mcqs


def trainer_generate_polls(request):
    questions = []
    if request.method == 'POST':
        form = PollGenerateForm(request.POST)
        if form.is_valid():
            topics = form.cleaned_data['topics'].split(',')
            n_questions = form.cleaned_data['n_questions']

            prompt = build_prompt(topics, n_questions)
            print("Prompt:", prompt)
            raw_output = ask_openrouter(prompt)
            print("=== RAW OUTPUT ===")
            print(raw_output)
            questions = parse_mcqs(raw_output)
            print("Parsed questions:", questions)

    else:
        form = PollGenerateForm()

    return render(request, 'trainer/polls/trainer_generate_polls.html', {
        'form': form,
        'questions': questions
    })