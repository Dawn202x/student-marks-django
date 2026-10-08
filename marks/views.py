import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mark, Profile
from .forms import MarkForm
from django.contrib.auth.models import User


@login_required
def add_mark_view(request):
    if not request.user.is_staff:
        return redirect("show_marks")
    if request.method == "POST":
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.user = request.user
            mark.save()
            return redirect("show_marks")
    else:
        form = MarkForm()
    return render(request, "add_mark.html", {"form": form})


@login_required
def show_marks(request):
    user_marks = Mark.objects.filter(user=request.user).values("name", "subject", "marks")
    df = pd.DataFrame(list(user_marks))
    if df.empty:
        return render(request, "marks.html", {
            "table": "<p>You have no marks yet.</p>", "average": 0,
            "subject_avg": {}, "has_chart": False, "is_admin": request.user.is_staff,
        })
    average_marks = df["marks"].mean()
    table_html = df.to_html(index=False)
    subject_avg = df.groupby("subject")["marks"].mean()
    static_dir = os.path.join(settings.BASE_DIR, "marks", "static", "marks")
    os.makedirs(static_dir, exist_ok=True)
    chart_filename = f"chart_{request.user.id}.png"
    chart_full_path = os.path.join(static_dir, chart_filename)
    plt.figure(figsize=(6, 4))
    plt.bar(df["name"], df["marks"], color="skyblue")
    plt.axhline(np.mean(df["marks"]), color="red", linestyle="--", label="Average")
    plt.xlabel("Student"); plt.ylabel("Marks"); plt.title("Your Marks"); plt.legend()
    plt.tight_layout(); plt.savefig(chart_full_path); plt.close()
    context = {
        "table": table_html, "average": round(average_marks, 2),
        "subject_avg": subject_avg.to_dict(), "has_chart": True,
        "chart_path": f"marks/{chart_filename}", "is_admin": request.user.is_staff,
    }
    return render(request, "marks.html", context)


def forgot_password_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        pin = request.POST.get("pin")
        new_password = request.POST.get("new_password")
        try:
            user = User.objects.get(username=username)
            if user.profile.pin_code == pin:
                user.set_password(new_password)
                user.save()
                return redirect("login")
            else:
                error = "Incorrect PIN."
        except User.DoesNotExist:
            error = "Username not found."
        except Profile.DoesNotExist:
            error = "No PIN set for this user. Contact admin."
    return render(request, "forgot_password.html", {"error": error})