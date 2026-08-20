from django.http import JsonResponse
from django.shortcuts import render
from HR import evaluate_resume
from files import extract_text_from_bytes
import zipfile
from io import BytesIO


def health(request):
    return JsonResponse({'status': 'ok'})


def home(request):
    results = []
    resume_text = ''
    desc_text = ''
    error = ''

    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')
        desc_text = request.POST.get('desc_text', '').strip()
        resume_text = request.POST.get('resume_text', '').strip()

        # If a ZIP was uploaded, extract multiple resumes and evaluate each
        if resume_file:
            filename = resume_file.name or ''
            ext = filename.split('.')[-1].lower()
            data = resume_file.read()

            try:
                if ext == 'zip':
                    with zipfile.ZipFile(BytesIO(data)) as z:
                        for member in z.namelist():
                            if member.endswith('/'):
                                continue
                            try:
                                member_bytes = z.read(member)
                                try:
                                    text = extract_text_from_bytes(member, member_bytes)
                                except Exception:
                                    text = ''
                                if text:
                                    eval_res = evaluate_resume(text, desc_text)
                                    results.append({'name': member, 'result': eval_res})
                                else:
                                    results.append({'name': member, 'error': 'Could not extract text'})
                            except Exception as exc:
                                results.append({'name': member, 'error': f'ZIP read error: {exc}'})
                else:
                    try:
                        resume_text = extract_text_from_bytes(filename, data)
                    except Exception as exc:
                        error = f'Unable to extract text from uploaded file: {exc}'
            except zipfile.BadZipFile:
                # Not a zip or corrupted; fall back to single file handling
                try:
                    resume_text = extract_text_from_bytes(filename, data)
                except Exception as exc:
                    error = f'Unable to extract text from uploaded file: {exc}'

        # Single resume evaluation (either pasted text or uploaded single file)
        if not results:
            if not resume_text or not desc_text:
                if not error:
                    error = 'Please provide both resume text and job description text, or upload a resume file.'
            else:
                try:
                    res = evaluate_resume(resume_text, desc_text)
                    results.append({'name': 'pasted_or_uploaded', 'result': res})
                except Exception as exc:
                    error = f'Error during evaluation: {exc}'

    successful_results = [item for item in results if not item.get('error')]
    leaderboard = sorted(
        successful_results,
        key=lambda item: int(item.get('result', {}).get('matching_score') or 0),
        reverse=True,
    )
    average_score = 0
    if leaderboard:
        average_score = round(
            sum(int(item.get('result', {}).get('matching_score') or 0) for item in leaderboard) / len(leaderboard)
        )

    return render(
        request,
        'evaluation/index.html',
        {
            'results': results,
            'leaderboard': leaderboard,
            'average_score': average_score,
            'resume_text': resume_text,
            'desc_text': desc_text,
            'error': error,
        },
    )
