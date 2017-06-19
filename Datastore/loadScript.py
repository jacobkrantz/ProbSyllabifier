from collections import OrderedDict
sc = SQLiteClient()
# these commands were run in other locations. Pooled together for history.

# 1st on 6/17
colsAndTypes = OrderedDict([("Word","TEXT"),("PhonCLX","TEXT"),("PhonCPA","TEXT"),("PhonDISC","TEXT"),("PhonSAM","TEXT"),("PronCnt","INTEGER")])
sc.createTable("pronunciations", colsAndTypes)
# 2nd on 6/17
colsAndTypes = OrderedDict([("Word","TEXT"),("WordCnt","INTEGER")])
sc.createTable("words", colsAndTypes)
# 3rd on 6/17
colsAndTypes = OrderedDict([("Word","TEXT"),("PhonSylCLX","TEXT"),("PhonSylCPA","TEXT"),("PhonSylDISC","TEXT"),("PhonSylSAM","TEXT"),("SylCnt","INTEGER"),("WordSyl","TEXT")])
sc.createTable("syllabifications", colsAndTypes)

#-------------------------------

# 1-3 ran in dataLoader.py
# 1st on 6/18       load the words table
cols = ["Word","WordCnt"]
dl.loadTableFromFile("words", "C:\Users\Jacob\Desktop\wordforms\words-1.txt", cols)
print "1 done"
dl.loadTableFromFile("words", "C:\Users\Jacob\Desktop\wordforms\words-2.txt", cols)
print "2 done"
dl.loadTableFromFile("words", "C:\Users\Jacob\Desktop\wordforms\words-3.txt", cols)
print "3 done"
dl.loadTableFromFile("words", "C:\Users\Jacob\Desktop\wordforms\words-4.txt", cols)
print "4 done"
dl.loadTableFromFile("words", "C:\Users\Jacob\Desktop\wordforms\words-5.txt", cols)
print "5 done"
# 2nd on 6/18       load the pronunciations table
cols = ["Word","PhonCLX","PhonCPA","PhonDISC","PhonSAM","PronCnt"]
dl.loadTableFromFile("pronunciations", "C:\Users\Jacob\Desktop\wordforms\pronunciations-1.txt", cols)
print "1 done"
dl.loadTableFromFile("pronunciations", "C:\Users\Jacob\Desktop\wordforms\pronunciations-2.txt", cols)
print "2 done"
dl.loadTableFromFile("pronunciations", "C:\Users\Jacob\Desktop\wordforms\pronunciations-3.txt", cols)
print "3 done"
dl.loadTableFromFile("pronunciations", "C:\Users\Jacob\Desktop\wordforms\pronunciations-4.txt", cols)
print "4 done"
dl.loadTableFromFile("pronunciations", "C:\Users\Jacob\Desktop\wordforms\pronunciations-5.txt", cols)
print "5 done"
# 3rd on 6/18       load the syllabifications table
cols = ["Word","PhonSylCLX","PhonSylCPA","PhonSylDISC","PhonSylSAM","SylCnt","WordSyl"]
dl.loadTableFromFile("syllabifications", "C:\Users\Jacob\Desktop\wordforms\syllabifications-1.txt", cols)
print "1 done"
dl.loadTableFromFile("syllabifications", "C:\Users\Jacob\Desktop\wordforms\syllabifications-2.txt", cols)
print "2 done"
dl.loadTableFromFile("syllabifications", "C:\Users\Jacob\Desktop\wordforms\syllabifications-3.txt", cols)
print "3 done"
dl.loadTableFromFile("syllabifications", "C:\Users\Jacob\Desktop\wordforms\syllabifications-4.txt", cols)
print "4 done"
dl.loadTableFromFile("syllabifications", "C:\Users\Jacob\Desktop\wordforms\syllabifications-5.txt", cols)
print "5 done"

#-------------------------------
