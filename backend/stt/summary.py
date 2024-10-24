from transformers import T5Tokenizer, T5ForConditionalGeneration

async def summarize(input_text: str) -> str:
    # Load the pre-trained Flan-T5 model and tokenizer
    model_name = "google/flan-t5-base"  # or try "flan-t5-base" for a larger model
    print(f'Model: {model_name}')
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # Define a messy paragraph for testing
    messy_paragraph = """
        The weather today, well, you know, it's kind of unpredictable, but they said on the news it might rain, 
        but who knows if that will happen, because sometimes they get it wrong, and, yeah, we were planning 
        to go for a picnic, but now we're unsure, maybe we'll just stay home, or maybe, I don't know, find an 
        indoor activity or something.
    """

    paragraph = """
        Alright, so, um, okay, picture this—like, imagine you're sketching, right? And it’s, you know, a modern French farmhouse kitchen. 
        You wanna start with, uh, you know, the big stuff first, right? So maybe, I dunno, like a huge, rustic wooden table in the center—kinda rough, 
        but charming, right? And then, like, on the side, maybe, uh, cabinets—white or, you know, light colors—just, you know, 
        keep it simple but classic. Oh, and don’t forget, like, uh, the big farmhouse sink, those, like, deep ones, right? 
        But when you're sketching, don’t make it too perfect, like, uh, rough lines, you know? And, oh! Throw in, like, 
        some hanging pots or something, but, like, not too precise—just, you know, have fun with it. 
        Make it feel, uh, lived-in, I guess? Yeah, like that.
    """

    # Prepare input prompt instructing cleanup and summarization
    # input_text = f"Clean up and summarize the following paragraph: {messy_paragraph}"

    # Tokenize the input and generate output
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=150, num_beams=5, early_stopping=True)

    # Decode and print the output
    clean_summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Cleaned up and summarized text:", clean_summary)
    return clean_summary


