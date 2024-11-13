from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol

import re

# removes non-alphabetic characters
REGEX = re.compile(r"\b[a-zA-Z]+\b")

# creates a unigram inverted index
# extends MRJob
class UnigramIndex(MRJob):  
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

        # cleans each word & yields (word, docID) pairs for reducer 
        for word in (REGEX.findall(doc_content.lower())):
            yield word, doc_id

    # custom reducer
    # handles aggregation operations (counts)
    def reducer(self, word, doc_ids):
        # create dict (map) to hold (docID, count) key-value pairs
        counts = {}
        
        # update map entries
        for doc_id in doc_ids:
            counts[doc_id] = counts.get(doc_id, 0) + 1
        
        # format postings for output
        counts_list = "\t".join([f"{doc_id}:{count}" for doc_id, count in counts.items()])
        
        yield None, f"{word}\t{counts_list}"


if __name__ == "__main__":
    UnigramIndex.run()