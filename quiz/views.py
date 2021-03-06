from django.contrib.auth.decorators import login_required
from django.db import transaction
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils.decorators import method_decorator
from Quizzes_Surveys.decorators import teacher_required, student_required
from .models import Quiz, Question, QuizResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from .forms import QuestionFormSet, QuizForm, TakeQuizForm
from users.models import Teacher, Subject, Batch
from django.contrib.auth.mixins import LoginRequiredMixin
import copy


# Create your views Question

@login_required
@student_required
def attempt_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    student = request.user.student

    if QuizResponse.objects.filter(quiz=quiz) == QuizResponse.objects.filter(student=student):
        return render(request, 'quiz/attempt.html')

    total_questions = questions.__len__()
    if request.method == 'POST':
        form = TakeQuizForm(data=request.POST, quiz=quiz)
        # if form.is_valid():
        #     with transaction.atomic():
        #         student_answer = form.save(commit=False)
        #         student_answer.student = student
        #         student_answer.save()
        #         for question in questions:
        #             student.
        #         # if student.get_unanswered_questions(quiz).exists():
        #         #     return redirect('students:take_quiz', pk)
        #         # else:
        #         #     correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
        #         #     score = round((correct_answers / total_questions) * 100.0, 2)
        #         #     QuizResponse.objects.create(student=student, quiz=quiz, score=score)
        #         #     if score < 50.0:
        #         #         messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
        #         #     else:
        #         #         messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
        #         #     return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(quiz=quiz)

    return render(request, 'quiz/attempt.html', {'form': form})


@teacher_required
@login_required
def add_quiz(request, pk=None):
    template_name = 'quiz/add_quiz.html'
    teacher = request.user.teacher
    if pk is None:
        if request.method == 'POST':
            form = QuizForm(teacher, request.POST)
            if form.is_valid():
                quiz = form.save(commit=False)
                quiz.title = form.cleaned_data['title']
                quiz.author = teacher
                quiz.subject = form.cleaned_data['subject']
                quiz.save()
                form.save_m2m()
                return redirect('edit-quiz', pk=quiz.pk)
        else:
            form = QuizForm(teacher)
    else:
        quiz = Quiz.objects.get(pk=pk)
        if request.method == 'POST':
            form = QuizForm(teacher, request.POST, hide_condition=True, initial={'subject': quiz.subject})
            if form.is_valid():
                new_quiz = form.save(commit=False)
                new_quiz.title = form.cleaned_data['title']
                new_quiz.author = teacher
                new_quiz.subject = form.cleaned_data['subject']
                new_quiz.save()
                form.save_m2m()
                for question in Question.objects.filter(quiz=quiz):
                    Question.objects.create(quiz=new_quiz, question=question.question, option_a=question.option_a,
                                            option_b=question.option_b, option_c=question.option_c,
                                            option_d=question.option_d, correct_ans=question.correct_ans)
                return redirect('edit-quiz', pk=new_quiz.pk)
        else:
            form = QuizForm(teacher, hide_condition=True, initial={'subject': quiz.subject})

    return render(request, template_name, {'form': form})


@teacher_required
@login_required
def edit_quiz(request, pk):
    template_name = 'quiz/edit_quiz.html'
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz).values()
    if request.method == 'GET':
        formset = QuestionFormSet(request.GET or None, initial=questions)
    elif request.method == 'POST':
        formset = QuestionFormSet(request.POST, initial=questions)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                text = form.cleaned_data.get('question')
                a = form.cleaned_data.get('option_a')
                b = form.cleaned_data.get('option_b')
                c = form.cleaned_data.get('option_c')
                d = form.cleaned_data.get('option_d')
                ans = form.cleaned_data.get('correct_ans')
                # save book instance
                if text:
                    Question(question=text, quiz=quiz, option_a=a, option_b=b, option_c=c, option_d=d,
                             correct_ans=ans).save()
            # once all books are saved, redirect to book list view
            return HttpResponse("<html><body>Created</body></html>")
    return render(request, template_name, {
        'formset': formset,
    })


def view_quiz(request, pk):
    # curr_teacher = request.user.teacher
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    context = {
        'questions': questions,
        'quiz': quiz
    }
    return render(request, 'quiz/view_quiz.html', context)
