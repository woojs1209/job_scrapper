from scrapper import start_scrapper
from save import save_to_file

jobs = start_scrapper()
save_to_file(jobs)