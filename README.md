#Nepali SpellCorrector

##Description
A spell corrector for Nepali that uses Edit Distance to predict correct words.

![Screenshot](https://cloud.githubusercontent.com/assets/4928045/10867454/287e1bbe-808b-11e5-8a6a-84139e7a42b3.png)

##Running
Checkout the latest sources with:

    git clone https://github.com/tnagorra/nspell

Compile the library with:

    python3 setup.py build_ext --inplace

Run the application with:

    python3 correctorN.py


##Todo
- [x] Calculate EditDistance and generate Candidates
- [x] Segmentation of words
- [ ] Correction of segmented words (connect and disconnet) using probability model
- [ ] Extract vocabulary from corpus
- [ ] Stemming of words
- [ ] Create Confusion matrix from corpus


##License
It is distributed under [GNU GPL][1]. A copy of the license is available in the distributed LICENSE file.

[1]: http://www.gnu.org/licenses/gpl.txt
