// These words have been generated from executing get_famous_quotes_in_list
// Source for the quotes: https://type.fit/api/quotes
// Since there are too much quotes to hold in the list I have reduced the number of quotes.
const QUOTE_LIST = [
    'Genius is one percent inspiration and ninety-nine percent perspiration.', 
    'You can observe a lot just by watching.', 
    'A house divided against itself cannot stand.', 
    'Difficulties increase the nearer we get to the goal.', 
    'Fate is in your hands and no one elses', 
    'Be the chief but never the lord.', 
    'Nothing happens unless first we dream.', 
    'Well begun is half done.', 
    'Life is a learning experience, only if you learn.', 
    'Self-complacency is fatal to progress.', 
    'Peace comes from within. Do not seek it without.', 
    'What you give is what you get.', 
    'We can only learn to love by loving.', 
    'Life is change. Growth is optional. Choose wisely.', 
    "You'll see it when you believe it.", 
    'Today is the tomorrow we worried about yesterday.', 
    "It's easier to see the mistakes on someone else's paper.", 
    'Every man dies. Not every man really lives.', 
    'To lead people walk behind them.', 
    'Having nothing, nothing can he lose.', 
    'Trouble is only opportunity in work clothes.', 
    'A rolling stone gathers no moss.', 
    'Ideas are the beginning points of all fortunes.', 
    'Everything in life is luck.', 
    'Doing nothing is better than being busy doing nothing.', 
    'Trust yourself. You know more than you think you do.', 
    'Study the past, if you would divine the future.', 
    'The day is already blessed, find peace within it.', 
    'From error to error one discovers the entire truth.', 
    'Well done is better than well said.', 
    'Bite off more than you can chew, then chew it.', 
    'Work out your own salvation. Do not depend on others.', 
    'One today is worth two tomorrows.', 
    'Once you choose hope, anythings possible.', 
    'God always takes the simplest way.', 
    'One fails forward toward success.', 
    'From small beginnings come great things.', 
    'Learning is a treasure that will follow its owner everywhere', 
    'Be as you wish to seem.', 'The world is always in movement.', 
    'Never mistake activity for achievement.', 
    'What worries you masters you.', 
    'One faces the future with ones past.', 
    'Goals are the fuel in the furnace of achievement.', 
    'Who sows virtue reaps honour.', 
    'Be kind whenever possible. It is always possible.', 
    "Talk doesn't cook rice.", 
    'He is able who thinks he is able.', 
    'A goal without a plan is just a wish.', 
    'To succeed, we must first believe that we can.', 
    'Learn from yesterday, live for today, hope for tomorrow.', 
    'A weed is no more than a flower in disguise.', 
    'Do, or do not. There is no try.', 
    'All serious daring starts from within.', 
    'The best teacher is experience learned from failures.', 
    'Think how hard physics would be if particles could think.', 
    "Love is the flower you've got to let grow.", 
    "Don't wait. The time will never be just right.", 
    'Time is the wisest counsellor of all.', 
    'You give before you get.', 
    'Wisdom begins in wonder.', 
    'Without courage, wisdom bears no fruit.', 
    'Change in all things is sweet.', 
    'What you fear is that which requires action to overcome.', 
    'When performance exceeds ambition, the overlap is called success.', 
    'When deeds speak, words are nothing.', 
    'Real magic in relationships means an absence of judgement of others.', 
    'I never think of the future. It comes soon enough.', 
    'Skill to do comes of doing.', 
    'Wisdom is the supreme part of happiness.', 
    'I believe that every person is born with talent.', 
    'Important principles may, and must, be inflexible.', 
    'The undertaking of a new action brings new strength.', 
    'The years teach much which the days never know.', 
    'Our distrust is very expensive.', 
    'All know the way; few actually walk it.', 
    'Great talent finds happiness in execution.', 
    'Faith in oneself is the best and safest course.', 
    'Courage is going from failure to failure without losing enthusiasm.', 
    'The two most powerful warriors are patience and time.', 
    'Anticipate the difficult by managing the easy.', 
    'Those who are free of resentful thoughts surely find peace.', 
    'A short saying often contains much wisdom.', 
    'It takes both sunshine and rain to make a rainbow.', 
    'A beautiful thing is never perfect.', 
    'Only do what your heart tells you.', 
    'Life is movement-we breathe, we eat, we walk, we move!', 
    'No one can make you feel inferior without your consent.', 
    'Argue for your limitations, and sure enough theyre yours.', 
    'Luck is what happens when preparation meets opportunity.', 
    'Victory belongs to the most persevering.', 
    'Love all, trust a few, do wrong to none.', 
    'In order to win, you must expect to win.', 
    'A goal is a dream with a deadline.', 
    'You can do it if you believe you can!', 
    "Set your goals high, and don't stop till you get there.", 
    'Every new day is another chance to change your life.', 
    'Smile, breathe, and go slowly.', 
    'Nobody will believe in you unless you believe in yourself.', 
    'Do more than dream: work.', 
    'No man was ever wise by chance.', 
    'Some pursue happiness, others create it.', 
    'He that is giddy thinks the world turns round.', 
    "Don't ruin the present with the ruined past.", 
    'Do something wonderful, people may imitate it.', 
    'We do what we do because we believe.', 
    'Do one thing every day that scares you.', 
    'If you cannot be silent be brilliant and thoughtful.', 
    'Who looks outside, dreams; who looks inside, awakes.', 
    'What we think, we become.', 
    'The shortest answer is doing.', 
    'All our knowledge has its origins in our perceptions.', 
    'The harder you fall, the higher you bounce.', 
    'Trusting our intuition often saves us from disaster.', 
    'Truth is powerful and it prevails.', 
    'Light tomorrow with today!', 
    'Silence is a fence around wisdom.', 
    'Society develops wit, but its contemplation alone forms genius.', 
    'The simplest things are often the truest.', 
    'Everyone smiles in the same language.', 
    'Yesterday I dared to struggle. Today I dare to win.', 
    'No alibi will save you from accepting the responsibility.', 
    'If you can dream it, you can do it.', 
    'It is better to travel well than to arrive.', 
    "Life shrinks or expands in proportion to one's courage.", 
    'You have to believe in yourself.', 
    'Our intention creates our reality.', 
    'Silence is a true friend who never betrays.', 
    'Character develops itself in the stream of life.', 
    'From little acorns mighty oaks do grow.', 
    "You can't stop the waves, but you can learn to surf.", 
    'Reality does not conform to the ideal, but confirms it.', 
    'Speak low, if you speak love.', 
    'A really great talent finds its happiness in execution.', 
    'Reality leaves a lot to the imagination.', 
    'The greatest remedy for anger is delay.', 
    'Growth itself contains the germ of happiness.', 
    "You can do what's reasonable or you can decide what's possible.",
    'Nothing strengthens authority so much as silence.', 
    'Wherever you go, go with all your heart.', 
    'The only real valuable thing is intuition.', 
    'Good luck is another name for tenacity of purpose.', 
    'Rainbows apologize for angry skies.', 
    "Friendship isn't a big thing. It's a million little things.", 
    'Time is the most valuable thing a man can spend.', 
    'Whatever happens, take responsibility.', 
    'Experience is simply the name we give our mistakes.', 
    'I think and that is all that I am.', 
    'A good plan today is better than a perfect plan tomorrow.', 
    "If the shoe doesn't fit, must we change the foot?", 
    'Each day provides its own gifts.', 
    'While we stop to think, we often miss our opportunity.', 
    "Life isn't about finding yourself. Life is about creating yourself.", 
    "To bring anything into your life, imagine that it's already there.", 
    'Begin to weave and God will give you the thread.', 
    'The more you know yourself, the more you forgive yourself.', 
    "Someone remembers, someone cares; your name is whispered in someone's prayers.", 
    'Without faith, nothing is possible. With it, nothing is impossible.', 
    'Once we accept our limits, we go beyond them.', 
    "Don't be pushed by your problems; be led by your dreams.", 
    'Whatever we expect with confidence becomes our own self-fulfilling prophecy.', 
    'Everything you can imagine is real.', 
    'Fear is a darkroom where negatives develop.', 
    'The truest wisdom is a resolute determination.', 
    'Life is the flower for which love is the honey.', 
    'Freedom is the right to live as we wish.', 
    'Change your thoughts, change your life!', 
    "Never ignore a gut feeling, but never believe that it's enough.", 
    'Loss is nothing else but change,and change is Natures delight.', 
    'Someone is special only if you tell them.', 
    'Today is the tomorrow you worried about yesterday.', 
    'There is no way to happiness, happiness is the way.', 
    'The day always looks brighter from behind a smile.', 
    'A stumble may prevent a fall.', 
    'He who talks more is sooner exhausted.', 
    'He who is contented is rich.', 
    'What we achieve inwardly will change outer reality.', 
    'Our strength grows out of our weaknesses.', 
    'We must become the change we want to see.', 
    'Happiness is found in doing, not merely possessing.', 
    'Put your future in good hands your own.', 
    'We choose our destiny in the way we treat others.', 
    'No snowflake in an avalanche ever feels responsible.', 
    'Fortune favours the brave.', 
    'I believe in one thing only, the power of human will.', 
    'The best way out is always through.', 
    'The mind unlearns with difficulty what it has long learned.', 
    'I destroy my enemies when I make them my friends.', 
    'No garden is without its weeds.', 
    'There is no failure except in no longer trying.', 
    'Kind words will unlock an iron door.', 
    'Problems are only opportunities with thorns on them.', 
    'Life is just a chance to grow a soul.', 
    'Mountains cannot be surmounted except by winding paths.', 
    'May our hearts garden of awakening bloom with hundreds of flowers.', 
    'Fortune befriends the bold.', 
    'Keep true to the dreams of thy youth.', 
    "You're never a loser until you quit trying.", 
    'Science is organized knowledge. Wisdom is organized life.', 
    'Knowing is not enough; we must apply!', 
    'Strong beliefs win strong men, and then make them stronger.', 
    'Autumn is a second spring when every leaf is a flower.', 
    'If you surrender to the wind, you can ride it.', 
    'Keep yourself to the sunshine and you cannot see the shadow.', 
    'Write your plans in pencil and give God the eraser.', 
    'Inspiration exists, but it has to find us working.'
];

// Constants for colours
const BEGINNER_COLOUR = '#eb4841';
const NOVICE_COLOUR = '#FF7F50';
const INTERMEDIATE_COLOUR = '#DD9B00';
const FAST_COLOUR = '#98af07';
const PROFESSIONAL_COLOUR = '#4cc35c';
const EXPERT_COLOUR = '#20C0B0';
const MASTER_COLOUR = '#6495ED';
const GRANDMASTER_COLOUR = '#6363B0';
const ENLIGHTENED_COLOUR = '#AA62B0';

// Global variables related to scoring
let score = 0;
let currentScore = document.getElementById("currentScore");
let aboutScore = document.getElementById('aboutScore');
aboutScore.style.visibility = 'hidden';

// Global variables related to the quotes
let currentQuote = document.getElementById("currentQuote");
let typedQuote = document.getElementById("typedQuote");
typedQuote.style.visibility = 'hidden';

// Global variables related to game status
let gameStatus = document.getElementById("gameStatus");
let gameLevel = document.getElementById("gameLevel");
let hasStarted = false;
let hasAlerted = false;
let gamePlaying = false;

// Global variables related to timing
let timeRemaining = 12.25; // 12 + 0.25 seconds
let currentTime = document.getElementById("timeRemaining");
let aboutTime = document.getElementById("aboutTime");
aboutTime.style.visibility = 'hidden'

// Global variable to submit the score
let scoreSubmit = document.getElementById("scoreSubmit"); 
scoreSubmit.style.visibility = 'hidden';

// Global variables for starting and restarting the challenge
let start = document.getElementById('start');
let restart = document.getElementById('restart');
restart.style.visibility = 'hidden';

let randomNumber; 

// Check input
function checkInput() {
	if(typedQuote.value == currentQuote.innerHTML) {
		gameStatus.innerHTML = "Correct!"; 
		gamePlaying = true; 
		timeRemaining = 12.25;
		score = score + 1; 
        currentScore.innerHTML = score; 

		// Select a new word from the QUOTE_LIST
		randomNumber = Math.floor(Math.random() * QUOTE_LIST.length); 
		currentQuote.innerHTML = QUOTE_LIST[randomNumber]; 
		typedQuote.value = ""; 

        // Make sure the submit button is hidden
        scoreSubmit.style.visibility = 'hidden';
	} 
	else {
		gameStatus.innerHTML = ""; 
		if(score == -1) {
			currentScore.innerHTML = 0; 
		} 
		else {
			currentScore.innerHTML = score; 
			scoreSubmit.value = score;
		}
	}
} 

// Find out the game status 
function getGameStatus () {
	if (currentScore.innerHTML <= 10) {
		gameLevel.innerHTML = "You are a beginner.";
		gameLevel.style.color = BEGINNER_COLOUR;
        aboutScore.style.color = BEGINNER_COLOUR;
	}
	else if (currentScore.innerHTML > 10 && currentScore.innerHTML <= 20) {
		gameLevel.innerHTML = "You are a novice.";
		gameLevel.style.color = NOVICE_COLOUR;
        aboutScore.style.color = BEGINNER_COLOUR;
	}
	else if (currentScore.innerHTML > 20 && currentScore.innerHTML <= 30) {
		gameLevel.innerHTML = "You are an intermediate player.";
		gameLevel.style.color = INTERMEDIATE_COLOUR;
        aboutScore.style.color = INTERMEDIATE_COLOUR;
	}
	else if (currentScore.innerHTML > 30 && currentScore.innerHTML <= 40) {
		gameLevel.innerHTML = "You are a fast player.";
		gameLevel.style.color = FAST_COLOUR;
        aboutScore.style.color = FAST_COLOUR;
	}
	else if (currentScore.innerHTML > 40 && currentScore.innerHTML <= 50) {
		gameLevel.innerHTML = "You are a professional player.";
		gameLevel.style.color = PROFESSIONAL_COLOUR;
        aboutScore.style.color = PROFESSIONAL_COLOUR;
	}
	else if (currentScore.innerHTML > 50 && currentScore.innerHTML <= 60) {
		gameLevel.innerHTML = "You are an expert in this game.";
		gameLevel.style.color = EXPERT_COLOUR;
        aboutScore.style.color = EXPERT_COLOUR;
	}
	else if (currentScore.innerHTML > 60 && currentScore.innerHTML <= 70) {
		gameLevel.innerHTML = "You are a master!";
		gameLevel.style.color = MASTER_COLOUR;
        aboutScore.style.color = MASTER_COLOUR;
	}
	else if (currentScore.innerHTML > 70 && currentScore.innerHTML <= 80) {
		gameLevel.innerHTML = "You are a grand master!!";
		gameLevel.style.color = GRANDMASTER_COLOUR;
        aboutScore.style.color = GRANDMASTER_COLOUR;
	}
	else if (currentScore.innerHTML > 80) {
		gameLevel.innerHTML = "You are enlightened!!!";
		gameLevel.style.color = ENLIGHTENED_COLOUR;
        aboutScore.style.color = ENLIGHTENED_COLOUR;
	}

	if (!gamePlaying && hasStarted) {
		gameStatus.innerHTML = "Game Over.";
		
		if (timeRemaining == 0) {
			scoreSubmit.style.visibility = 'visible';
			restart.style.visibility = 'visible';
			typedQuote.style.visibility = 'hidden';
            if (!hasAlerted) {
                scoreSubmit.value = score;
				alert("Game over. Your score is " + score);
				hasAlerted = true;
			}
			score = -1;
		}
	}
}

function timer() {
	// Case: time is remaining
	if (timeRemaining > 0) {
		timeRemaining = timeRemaining - 0.25; 
	} 
	// Case: time over
	else if (timeRemaining == 0) { 
		gamePlaying = false;
	} 
	currentTime.innerHTML = timeRemaining;
} 

// Executed when the user presses the start button
function beginSentenceTyping() { 
    start.style.visibility = 'hidden';
	hasStarted = true;
    hasAlerted = false;
	gamePlaying = true; 
	typedQuote.style.visibility = 'visible';
    aboutTime.style.visibility = 'visible';
	aboutScore.style.visibility = 'visible';
	scoreSubmit.style.visibility = 'hidden';

	// Select a word from the SAT word list
	randomNumber = Math.floor(Math.random() * QUOTE_LIST.length); 
	currentQuote.innerHTML = QUOTE_LIST[randomNumber]; 
	gameLevel.innerHTML = ""

	// Add a method to check the input of the word from the user
	typedQuote.addEventListener("input", checkInput);
    // Check the game status every 10 milli-second
	setInterval(getGameStatus, 10); 
	// Check and update the timer every 0.25 second
	setInterval(timer, 250);  
} 