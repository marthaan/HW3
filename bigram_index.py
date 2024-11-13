from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol

import re

# removes non-alphabetic characters
REGEX = re.compile(r"\b[a-zA-Z]+\b")

# desired bigrams for output (given by assignment)
SELECTED_BIGRAMS = {"computer science", "information retrieval", "power politics", "los angeles", "bruce willis"}

# creates a bigram inverted index for select bigrams
# extends MRJob
class BigramIndex(MRJob):  
    # remove automatic quotes from MRJob output
    OUTPUT_PROTOCOL = RawValueProtocol

    # defines sequence of MR steps
    def steps(self):
        return [MRStep(mapper = self.mapper, reducer = self.reducer)]
    
    # custom mapper
    # handles input preprocessing
    def mapper(self, _, line):
        # split doc ID from rest of doc content
        try: 
            doc_id, doc_content = line.split("\t", 1)
        except ValueError:
            return
        
        # cleans each word
        words = REGEX.findall(doc_content.lower())

        # forms bigrams & yields (bigram, docID) pairs for reducer 
        for idx in range(len(words) - 1):
            bigram = f"{words[idx]} {words[idx + 1]}"
            
            if bigram in SELECTED_BIGRAMS:
                yield bigram, doc_id         

    # custom reducer
    # handles aggregation operations (counts)
    def reducer(self, bigram, doc_ids):
        # create dict (map) to hold (docID, count) key-value pairs
        counts = {}
        
        # update map entries
        for doc_id in doc_ids:
            counts[doc_id] = counts.get(doc_id, 0) + 1
        
        # format postings for output
        counts_list = "\t".join([f"{doc_id}:{count}" for doc_id, count in counts.items()])
        
        yield None, f"{bigram}\t{counts_list}"

if __name__ == "__main__":
    BigramIndex.run()