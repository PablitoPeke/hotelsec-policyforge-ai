"""Validate student-supplied delivery facts; never infer a group, hours or video evidence."""
import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

REQUIREMENTS = tuple([f"RF-{i:02}" for i in range(1, 14)]
                     + [f"RNF-{i:02}" for i in range(1, 8)]
                     + [f"RE-{i:02}" for i in range(1, 4)])


def timestamp_seconds(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{2,3}:[0-5]\d", value):
        raise ValueError("Usa MM:SS.")
    minutes, seconds = map(int, value.split(":"))
    return minutes * 60 + seconds


def validate_delivery(data):
    pending = []
    group = data.get("group_number")
    individual = (group is None and data.get("submission_mode") == "individual"
                  and isinstance(data.get("author"), str) and bool(data["author"].strip()))
    if not individual and (type(group) is not int or not 1 <= group <= 99):
        pending.append("Numero real de grupo (1-99), o declaracion explicita de entrega individual con autor y sin numero.")
    hours = data.get("estimated_student_hours", {})
    if not hours or any(type(v) not in (int, float) or not 0 <= v <= 10000 for v in hours.values()):
        pending.append("Estimacion personal valida de horas por actividad.")
    video = data.get("video", {})
    try:
        url = urlsplit(video.get("url") or "")
        valid_url = url.scheme == "https" and bool(url.hostname) and not url.username and not url.password
    except ValueError:
        valid_url = False
    if not valid_url:
        pending.append("Enlace HTTPS del video, sin credenciales.")
    duration = video.get("duration_seconds")
    if type(duration) is not int or duration < 600:
        pending.append("Video real de al menos 600 segundos.")
    if video.get("format") != "mp4":
        pending.append("Video en formato MP4.")
    if (type(video.get("width")) is not int or type(video.get("height")) is not int
            or video["width"] < 1280 or video["height"] < 720):
        pending.append("Resolucion de video al menos 1280x720.")
    if video.get("access_checked_in_incognito") is not True:
        pending.append("Comprobar permisos del enlace de video en incognito.")
    for requirement in REQUIREMENTS:
        try:
            seconds = timestamp_seconds(video.get("timestamps", {}).get(requirement))
            if type(duration) is not int or seconds > duration:
                raise ValueError("Fuera de duracion.")
        except ValueError:
            pending.append(f"Minuto real MM:SS de {requirement} dentro del video.")
    external = data.get("external_installation", {})
    if external.get("completed") is not True or not all(external.get(k) for k in ("tester_alias", "date", "result")):
        pending.append("Instalacion siguiendo README por persona ajena al grupo y registro de resultado.")
    if data.get("student_pdf_reviewed") is not True:
        pending.append("Revision personal del PDF definitivo.")
    if data.get("narrative_updated_for_submission") is not True:
        pending.append("Actualizar parrafos de estado de memoria_content.json con video y comprobaciones ya realizados.")
    if data.get("repository_access_checked") is not True:
        pending.append("Comprobar acceso del docente al repositorio.")
    return pending


def submission_filename(data):
    group = data.get("group_number")
    if type(group) is int and 1 <= group <= 99:
        return f"P3_Grupo{group:02}_Memoria.pdf"
    if group is None and data.get("submission_mode") == "individual":
        author = unicodedata.normalize("NFKD", data.get("author", "")).encode("ascii", "ignore").decode()
        name = re.sub(r"[^A-Za-z0-9]+", "_", author).strip("_")
        if name:
            return f"P3_{name}_Memoria.pdf"
    raise ValueError("Falta grupo real o entrega individual explicitamente declarada.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, default=Path(__file__).resolve().parents[1] / "docs/practica3/delivery_metadata.json")
    args = parser.parse_args()
    data = json.loads(args.metadata.read_text(encoding="utf-8"))
    pending = validate_delivery(data)
    if pending:
        print("Pendientes documentales/manuales; no equivalen a fallos de la app:")
        for item in pending:
            print("- " + item)
        return 1
    print("Datos de entrega completos segun lo declarado. Revisar PDF renderizado, commit, tag y envio al campus.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
