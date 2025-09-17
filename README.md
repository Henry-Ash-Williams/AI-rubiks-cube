# Rubiks Cube & AI 

~~I'm not sure what question I'm trying to answer yet. All I know is that I have a script for scraping [reco.nz](https://reco.nz/) for valid 3x3 reconstructions, and a tokenizer for turning these moves into something that can be used by a model.~~

~~I'll figure out what I'm actually doing later.~~

## Ideas 

### Is Solved? 

> Given a sequence of scramble + solve, can we determine if it will produce a solved cube or not? 

- LSTM - No, see `notebooks/lstm-is-solved.ipynb` 
- BERT - In progress 

### [TODO] Solve 

> Given a scramble, can we produce a sequence of moves that will result in a solved cube?

#### Plan 

1. MaskedLM on solution sequence for a given scramble 
2. Next sentence prediction using pretrained model  

### [TODO] Reverse Scramble 

> Given a sequence of moves that produce a solved cube, can we produce the scramble that will produce a solved cube when this sequence of moves is applied to it? 

## TODO 

- [ ] Make a way to display a cube with a given permutation
- [ ] Better synthetic data generation 
- [ ] Better random move sequence generation 
- [ ] Extend beyond 3x3 solves? 