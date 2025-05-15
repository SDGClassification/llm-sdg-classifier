from sdgclassification.benchmark import Benchmark

from classifiers.chatgpt_meike.chatgpt_meike import Classifier

classifier = Classifier(config=1)
benchmark = Benchmark(classifier.classify, sdgs=[10])

benchmark.run()
