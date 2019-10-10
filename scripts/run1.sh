### need to have intder.in intder.out intder_template in the running dir
cp intder.* .
cp ref.int .
gen-refe.py
write_anpss_input.py anpass.in ./ ./ c2v
anpass.x < anpass.in > anpass.out
write_anpss_input.py anpass2.in ./ ./ c2v
anpass.x < anpass2.in > anpass2.out
run.py
write_intder_input.py intder_freqs.in ./
Intder2005 < intder_freqs.in > intder_freqs.out
run.sh
