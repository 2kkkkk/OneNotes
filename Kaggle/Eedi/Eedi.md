# Eedi

A Diagnostic Question is a multiple-choice question with four options: one correct answer and three distractors (incorrect answers). Each distractor is carefully crafted to capture a specific misconception.

Tagging distractors with appropriate misconceptions.

## My story

阅读了高vote的public notebook后，我认识到这个比赛的流程是recall+rerank。

对于recall，public notebook的方法是    用

```python
task='Given a math question with correct answer and a misconcepted incorrect answer, retrieve the most accurate misconception for the incorrect answer.'

query_text =f"### SubjectName: {row['SubjectName']}\n### ConstructName: {row['ConstructName']}\n### Question: {row['QuestionText']}\n### Correct Answer: {correct_answer}\n### Misconcepte Incorrect answer: {option}.{row[f'Answer{option}Text']}"
```

构建数据集,通过contrastive learning 和 hard negative mining 来finetune sft或者qwen-14b,最后通过与misceptions库的emedding进行匹配来recall。

但是没有公开的finetune代码，只有将别人微调好的lora直接拿来用。

对于recall，我不会微调，所以我的想法是，只用subjectname , constructname（再加上llm总结 的question关键句）再加上自己设计的promt（what are misconceptions that might happens in a math problem under this subjectname and constructname?） 来进行召回，模型用现成的mteb中的模型。

尝试了bge-large，bge-icl，bge-embedder, stella_en,以及不同的subject_construct+question+answer组合，但提交后结果较差，0.29左右，此时我决定还是直接用public notebook中人家已经Finetune好的Lora模型吧。



对于Rerank，public kernel是用QW32B+logits_zoo，选出最优的一个，其他24个直接用recall的排序结果。

我在查mteb时，我发现有bge 的reranker model,"reranker model uses question and documents as input and directly output the similarity instead of embedding"，我一看这不是就适合rerank任务嘛，于是我打算试试reranker模型，但是后面我一想，其实reranker模型也是llm的一种，本质是一样，可能还不如直接问llm。于是我从两方面优化public 的rerank部分：

1） 我想起discussion https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/540759中看到的，the trick of using LLM is:

- understand that LLM is just a parrot, it does not reason,plan . it doesn't even understand language
- always think of how to increase "the conditional probability" of "generating" your desired answer, rather than the logic to get your answer

于是我change了 prompt ，在prompt中加入了background 知识和一个example，对于public的qw14B模型，分数提升了0.02，排名直接到200，但是对于public的sft model，分数降了，但是我只在意提升，觉得是sft模型不够好的原因，**现在想想其实调prompt不应该以public lb的结果作为评判标准，是容易过拟合的一种行为。** 分数提升后，我又纠结尝试在prompt中加入更多例子，但是影响不大？（而且会超时）。

2）public kernel中用QW32B+logits_zoo，选出最优的一个，只survive了一次，因此我尝试survive 两次和三次，分数提高了，这个对于public sft 和public qwen14b两个模型最后分数都提升了，**这才是robust的做法**。



我在discussion中还看到有人尝试用qw72b代替32b来rerank，我尝试了但结果降低了一点，我就没用，但是private 公布后score其实提高了很多。



对于robust的答案选择，我的做法是前3个答案用qw14b模型及rerank的结果 ，后22个结果直接用sub+con+quetion 用没微调的bge-large计算embedding similarity召回的结果。**现在想想，兜底也要考虑偏差，不用偏差太大了，public lb分数很低，那么private lb 的分数也没太大的希望。兜底robust应该用更稳健的方法，比如这个比赛中用qw72b代替32b来rerank，虽然public lb 分数降低了一点（跟这个比赛score的波动相比其实无所谓），但是private lb的分数提高很大；再比如文章评分的比赛中，train_data中过滤掉分数小于3的学生文章，虽然public lb 没提高，但是private lb提高很大。这些理论上robust的做法，当在public lb的分数没有大的进步时，需要注意并采用。**



我应该尝试用0.48那个kernelhttps://www.kaggle.com/code/anhvth226/eedi-11-21-14b的，虽然跑不动，但是有Lora模型，应该自己调试一下。

## Top solutions

## 有代码

### 1st Place Detailed Solution

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551688

- [Training code](https://github.com/rbiswasfc/eedi-mining-misconceptions)
- [Inference Notebook](https://www.kaggle.com/code/conjuring92/eedi-a2-pipeline?scriptVersionId=211785645)
- [Dataset with Synthetic + Competition MCQ](https://www.kaggle.com/datasets/conjuring92/eedi-mcq-dataset)
- [CoT Dataset](https://www.kaggle.com/datasets/conjuring92/eedi-cot-sonnet-6k)

### 5th Place Solution

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391

https://github.com/ebinan92/Eedi-5th-solution?tab=readme-ov-file



### Efficiency 2nd Place Solution

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/552686

- https://www.kaggle.com/code/rsakata/eedi-1-misconception-explanation
- https://www.kaggle.com/code/rsakata/eedi-2-train-embedding-model
- https://www.kaggle.com/code/rsakata/eedi-3-retrieval

train-embedding-model这个代码我看了，并做了注释。

### 3rd Place Solution (with Magic Boost)

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551498

The inference code can be found at:
https://www.kaggle.com/code/threerabbits/eedi-11-21-myq14b-q32b-rerank-mod-novel-local-suf

**Let's Experiment**

On the second-to-last day of the competition (yes, I really dared to use two submissions for experiments at this point XD), I did this LB probing:

- Predicted only 1 misconception per question
- Tested twice:
  1. Using only seen misconceptions from training data: got 0.154
  2. Using only unseen misconceptions: got 0.444

Seeing these results, I made a bold guess that the seen-to-unseen ratio in the testing data was roughly 1:3.

**The Final Magic Touch**

So I implemented a simple post-processing:

- Multiplied the probabilities of all predicted unseen misconceptions by a constant C
- Adjusted until unseen misconceptions made up 75% of the first predictions

This little magic trick made the scores skyrocket 😮:

- Public LB: 0.590 → 0.658
- Private LB: 0.564 → 0.600

### 8th Place Solution

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551412

- Inference code: https://www.kaggle.com/code/yannan90/eedi-recall-rerank-lb-0-601-pb-0-584
- Training & Quantization code: https://github.com/yannan90/kaggle-2024-Eedi-8th-place-training-code

### 4th Place Solution

takoi part : https://github.com/TakoiHirokazu/kaggle-Eedi-4th-solution
charmq part : https://github.com/charmq00/kaggle_eedi_public
Inference : https://www.kaggle.com/code/charmq/eedi-pp040-ret15-exp345-341-348-multi-32b-ret-c015

### 2nd place solution

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551651

train code: [https://github.com/wangqihanginthesky/Eedi_kaggle\](https://github.com/wangqihanginthesky/Eedi_kaggle/)
inference code: https://www.kaggle.com/code/honglihang/2nd-place-inference-code

### (Almost) Zero-Shot Solution - Private 64h

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551449

### 31st place solution

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/553317

I finetuned (lora) a Qwen2.5-32b-awq reranker via trl.SFTTrainer. Here are my hyper parameters

My demo training notebook: https://www.kaggle.com/code/doublezeta/train-reranker Actually I did the training in Colab.

### 94th Bronze Solution Summary (only public notebooks with simple tricks)

https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551396

1. - Rerank only the first 3 candidates and focus on precision: I predicted the answer for 3 shuffled lists of misconceptions (because LLMs are biased to answers position), then take the answer only if it was chosen in all attempts.



## 需要learning

还是要自己会finetune

contrastive learning

embedding model (sentence transformer) BGE

flag embedding

flash attention

lora_config(task_type='casual_llm'和'feature_extract'的区别)