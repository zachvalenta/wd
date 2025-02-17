help:
	@echo
	@echo "======================================================================"
	@echo "db:       open litecli"
	@echo "find:     find potential FKs btw two CSVs"
	@echo "erd:      render ERD"
	@echo "======================================================================"
	@echo

db:
	litecli db.sqlite

# find:
# 	python find_fk.py $(tbl1) $(tbl2)

# erd:
# 	d2 --watch erd.d2 erd.svg
