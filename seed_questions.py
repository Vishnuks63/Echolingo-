from database import SessionLocal, Question
from ai_service import translation_service

def seed_questions():
    questions = {
        'beginner': [
            "What is the right way of saying 'Hello, how are you?' in this language?",
            "What is the right way of saying 'My name is John' in this language?",
            "What is the right way of saying 'Thank you very much' in this language?",
            "What is the right way of saying 'Good morning' in this language?",
            "What is the right way of saying 'Nice to meet you' in this language?"
        ],
        'intermediate': [
            "What is the right way of saying 'I would like to learn your language' in this language?",
            "What is the right way of saying 'What is your favorite food?' in this language?",
            "What is the right way of saying 'Where do you live?' in this language?",
            "What is the right way of saying 'How was your day?' in this language?",
            "What is the right way of saying 'Can you help me please?' in this language?"
        ],
        'advanced': [
            "What is the right way of saying 'Language learning opens new opportunities' in this language?",
            "What is the right way of saying 'Cultural exchange is very important' in this language?",
            "What is the right way of saying 'What are your future plans?' in this language?",
            "What is the right way of saying 'Let's discuss global topics' in this language?",
            "What is the right way of saying 'Share your thoughts about this' in this language?"
        ]
    }


    original_phrases = {
        'beginner': [
            "Hello, how are you?",
            "My name is John",
            "Thank you very much",
            "Good morning",
            "Nice to meet you"
        ],
        'intermediate': [
            "I would like to learn your language",
            "What is your favorite food?",
            "Where do you live?",
            "How was your day?",
            "Can you help me please?"
        ],
        'advanced': [
            "Language learning opens new opportunities",
            "Cultural exchange is very important",
            "What are your future plans?",
            "Let's discuss global topics",
            "Share your thoughts about this"
        ]
    }

    languages = ['hindi', 'tamil', 'telugu', 'marathi', 'bengali']
    db = SessionLocal()

    try:
        for language in languages:
            for level, questions_list in questions.items():
                for i, question in enumerate(questions_list):
                    
                    correct_translation = translation_service.translate(
                        original_phrases[level][i], 
                        language
                    )
                    
                    
                    wrong_phrases = [
                        f"Hello, good day",  
                        f"Hi there, how are you",  
                        f"Greetings, nice day"  
                    ]
                    
                    wrong_translations = [
                        translation_service.translate(phrase, language)
                        for phrase in wrong_phrases
                    ]
                    
                    
                    wrong_translations = [t for t in wrong_translations if t and t != correct_translation]
                    while len(wrong_translations) < 3:  
                        new_wrong = translation_service.translate(f"Wrong phrase {len(wrong_translations)}", language)
                        if new_wrong and new_wrong not in wrong_translations and new_wrong != correct_translation:
                            wrong_translations.append(new_wrong)
                    
                    
                    question_obj = Question(
                        english_text=original_phrases[level][i], 
                        translated_text=correct_translation,     
                        options=wrong_translations + [correct_translation],  
                        correct_answer=correct_translation,
                        language=language,
                        level=level
                    )
                    db.add(question_obj)
                    print(f"Added question for {language} - {level}")
        
        db.commit()
        print("Questions seeded successfully!")
    except Exception as e:
        print(f"Error seeding questions: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()