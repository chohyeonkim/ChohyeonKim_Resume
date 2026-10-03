"""Build separate before- and after-graduation resumes."""

import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


@dataclass(frozen=True)
class ResumeVariant:
    name: str
    graduation_status: str
    destination: str


VARIANTS = (
    ResumeVariant("after", "Graduated", "After Graduation/Chohyeon_Resume.pdf"),
    ResumeVariant("before", "Nov 2026", "Before Gradutation/ChoHyeon_Kim_Resume.pdf"),
)


class ResumeRepository:
    def __init__(self, root: Path):
        self.root = root

    def publish(self, build_directory: Path) -> None:
        for variant in VARIANTS:
            source = build_directory / f"resume-{variant.name}.pdf"
            destination = self.root / variant.destination
            shutil.copy2(source, destination)
            print(f"Updated: {destination}")
        shutil.copy2(build_directory / "resume-after.pdf", self.root / "resume.pdf")
        print("Updated: resume.pdf (after graduation)")


class ResumeBuildService:
    def __init__(self, repository: ResumeRepository):
        self.repository = repository

    def build(self, compiler: str) -> None:
        executable = shutil.which(compiler)
        if executable is None:
            raise FileNotFoundError(
                "pdflatex was not found. Add it to PATH or use --pdflatex with its full path."
            )

        with TemporaryDirectory(prefix="resume-build-") as temporary_directory:
            build_directory = Path(temporary_directory)
            for variant in VARIANTS:
                print(f"Building {variant.name}: {variant.graduation_status}", flush=True)
                latex_input = (
                    rf"\def\ResumeGraduationStatus{{{variant.graduation_status}}}"
                    r"\input{resume.tex}"
                )
                # Each variant has separate auxiliary files; run twice for references.
                for _ in range(2):
                    subprocess.run(
                        [
                            executable,
                            "-interaction=nonstopmode",
                            "-halt-on-error",
                            f"-output-directory={build_directory}",
                            f"-jobname=resume-{variant.name}",
                            latex_input,
                        ],
                        cwd=self.repository.root,
                        check=True,
                    )
                if not (build_directory / f"resume-{variant.name}.pdf").is_file():
                    raise FileNotFoundError(f"No PDF was generated for {variant.name}.")

            # Publish only after both variants compile successfully.
            self.repository.publish(build_directory)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdflatex", default="pdflatex", help="Path to pdflatex")
    args = parser.parse_args()

    repository = ResumeRepository(Path(__file__).resolve().parent)
    try:
        ResumeBuildService(repository).build(args.pdflatex)
    except subprocess.CalledProcessError:
        print(
            "LaTeX compilation failed. See the output above. Existing PDFs were not updated.",
            file=sys.stderr,
        )
        return 1
    except OSError as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
