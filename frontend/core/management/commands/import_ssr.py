from django.core.management.base import BaseCommand
from core.models import CSSR, SSR, ISSR, VNTR
from pathlib import Path

class Command(BaseCommand):
    help = "Import data into the database"

    def add_arguments(self, parser):
        parser.add_argument('dirpath', type=str, help='Path to the directory with the files')

    def handle(self, *args, **kwargs):
        dirpath = Path(kwargs['dirpath'])

        if not dirpath.exists() or not dirpath.is_dir():
            self.stderr.write(self.style.ERROR(f"Invalid directory: {dirpath}"))
            return
            
        files = list(dirpath.glob('*.txt'))


        for file in files:
            self.stdout.write(f"Importing {file.name}...")
            clade_parts = file.name.split('_')
            clade = f"{clade_parts[0]}"

            with file.open('r') as f:
                lines = f.readlines()

                if not lines:
                    self.stderr.write(self.style.warning(f"{file.name} is empty"))
                    continue

                for line in lines:
                    aux = line.split('\t')
                    obj = SSR(
                        sequence = aux[1],
                        motif = aux[3],
                        start = aux[6],
                        end = aux[7],
                        length = aux[8],
                        clade = clade,
                        standard = aux[2],
                        type = aux[4],
                        repeat = aux[5]
                    )
                    obj.save()
        self.stdout.write(self.style.SUCCESS("All files imported successfully"))

