I originally coded most of this project in Replit using Java as assigned, 
but continued to run into configuration errors with Replit (depsite it working
in smaller cases and meeting with TAs about anything I was misunderstanding, 
which did not seem to be the case). Thus, I chose to try a different route using 
MapReduce in Python using the MRJob library, which proved to be much more straightforward in 
terms of configuration. MRJob enabled simplified use/flexibility, allowing me to 
translate the Java code I had already writen to Python, and have it work locally 
as I intended it to with Replit. Overall, I chose to do this so that I can focus on 
the core MapReduce logic that I had already understood/implemented, but with less 
complexity when it came to testing and execution.

With this program, I decided to create separate scripts for the unigram index 
and bigram index, while using the same reducer for both. Both mappers have the 
same functionalities/design as the provided mapper in Java. It separated/extracted the 
doc ID from the rest of the doc content, cleans the input words to be only lowercase 
and alphabetic, and yield (unigram or bigram, docID) pairs as intermittent data for the 
reducer. The main difference between the two mappers was forming the bigrams using 
adjacent indices. A stepper is also included as it is in the Java code, since this is 
an important part of structuring a MapReduce job no matter the language. 
Other things to note within the scripts would be using the RawValueProtocol.
This was because MRJob automatically outputs words and their postings within quotations, 
which was not desired (both in this assignment but also because the Java format did not 
have this in general). I did attempt to sort the output alphabetically, but this is complex
with MRJob's automatic configurations. Since it isn't specifically required in the assignment, 
I opted to skip this step. 

Lastly, I was also facing very long delays and some timeouts with using the provided 
large data, so I opted to use the alternative data towards the end of the assignment 
that is shorter. This worked quickly and efficiently both for testing and final output, 
while still obtaining a sufficient amount of words for the unigram index and enough 
occurrences for the selected bigrams (to ensure the bigram index still worked as intended 
even with much less data). 

To execute unigram_index.py: python unigram_index.py data/fulldata > out/unigram_index.txt
To execute bigram_index.py: python bigram_index.py data/devdata > out/selected_bigram_index.txt