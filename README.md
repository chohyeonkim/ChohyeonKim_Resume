# ChoHyeon Kim — Resume

This repository contains the LaTeX source code and compiled PDF for my Software Engineering resume.

📄 **[After Graduation Resume (PDF)](<./After%20Graduation/Chohyeon_Resume.pdf>)**
📄 **[Before Graduation Resume (PDF)](<./Before%20Gradutation/ChoHyeon_Kim_Resume.pdf>)**

---

## 🛠️ Build from Source

To compile locally, install Python 3 and a TeX distribution (e.g., TeX Live, MacTeX, or MiKTeX), then run:

```powershell
python build_resume.py
```

The script compiles two versions of `resume.tex`, running `pdflatex` twice per
version. Only the UBC graduation status changes:

- `After Graduation/Chohyeon_Resume.pdf`: `Graduated`
- `Before Gradutation/ChoHyeon_Kim_Resume.pdf`: `Nov 2026`

After both versions compile successfully, the script overwrites the two folder
PDFs and updates the root `resume.pdf` with the after-graduation version.
The Kookmin University status remains `Graduated`. The source file is not
rewritten during the build, and temporary build files are cleaned up automatically.

If `pdflatex` is not on your PATH, specify its location:

```powershell
python build_resume.py --pdflatex 'C:\Users\Elly\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
```

Running `pdflatex resume.tex` directly only updates the root PDF; use the script
to update the folder copies as well.
