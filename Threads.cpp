/*
 * Threads.cpp
 *
 *  Created on: Oct 31, 2022
 *  Completed on: Nov 18, 2022
 *      Author: Justin Sengenberger
 */

// Libraries
#include <exception>
#include <iostream>
#include <mutex>
#include <thread>
using namespace std;

// Constants
const bool UP = true;
const bool DOWN = false;
const int MAX = 20;
const int MIN = 0;
const size_t MAXTHREADS = 2;

// Classes
class Counter
{
	private:
		bool direction;
		int count;

	public:
		// Constructors
		Counter()
		{
			try
			{
				direction = retrieveDirection();
				setCount(retrieveStartNum());
			}
			catch (const char* msg)
			{
				// Error on Failed Input
				cout << "\n";
				cerr << "User Input Error: " << msg << endl;
				cerr << "Executing Default - Increment from Zero" << endl;
				cout << "\n";

				// Assume starting UP from MIN
				direction = UP;
				count = MIN;
			}
		}
		Counter(bool startDir, int startNum)
		{
			direction = startDir;
			setCount(startNum);
		}

		// Getters
		bool getDirection()
		{
			return direction;
		}
		int getCount()
		{
			return count;
		}

		// Setters
		void setDirection(bool input)
		{
			direction = input;
		}
		void setCount(int input)
		{
			// Keep MIN / MAX Bounds
			if (input < MIN)
			{
				cout << "\n";
				cout << "Start Too Low - Default: MIN";
				cout << "\n";

				input = MIN;
			}
			else if (input > MAX)
			{
				cout << "\n";
				cout << "Start Too High - Default: MAX";
				cout << "\n";

				input = MAX;
			}

			count = input;
		}

		// Count Methods
		void countDown ()
		{
			cout << count;

			while (count > MIN)
			{
				count--;
				cout << " - " << count;
			}

			cout << "\n";
			cout << "\n";
			cout << "MIN Reached" << endl;
			cout << "\n";
		}
		void countUp ()
		{
			cout << count;

			while (count < MAX)
			{
				count++;
				cout << " - " << count;
			}

			cout << "\n";
			cout << "\n";
			cout << "MAX Reached" << endl;
			cout << "\n";
		}

	private:
		// User Input
		bool retrieveDirection ()
		{
			string* userInput = nullptr;

			try
			{
				userInput = new string;			// throws at lack of memory

				cout << "Do you want to count up to start? Enter Y/N: ";
				cin >> *userInput;

				// Check Input
				if ((userInput[0] == "y") || (userInput[0] == "Y"))
				{
					direction = UP;
				}
				else if ((userInput[0] == "n") || (userInput[0] == "N"))
				{
					direction = DOWN;
				}
				else
				{
					throw "(Y)es or (N)o Required";
				}

				delete userInput;
				return direction;
			}
			catch (bad_alloc&)
			{
				delete userInput;
				throw "Bad Allocation";			// out of memory
			}
			catch (const char* msg)
			{
				delete userInput;
				throw msg;						// invalid input or other error
			}
		}
		int retrieveStartNum ()
		{
			string* userInput = nullptr;
			try
			{
				userInput = new string;			// throws at lack of memory

				cout << "Enter a number within " << MIN << " and " << MAX << " to start the counter: ";
				cin >> *userInput;

				// Declare Conversion Variables
				string toInt;
				bool neg = false;

				// Check Input
				for (char const c : *userInput)
				{
					// Consider Negatives
					if (c == '-')
					{
						neg = true;
					}
					else if (isdigit(c) == false)
					{
						throw "Non-Integer Input";
					}
					else
					{
						toInt += c;
					}
				}

				// Perform Conversion
				int startNum = stoi(toInt);		// throws at too large of integer

				if (neg == true)
				{
					startNum = startNum * -1;
				}

				delete userInput;
				return startNum;
			}
			catch (bad_alloc&)
			{
				delete userInput;
				throw "Bad Allocation";			// out of memory
			}
			catch (out_of_range&)
			{
				delete userInput;
				throw "Integer Overflow";		// integer too large
			}
			catch (const char* msg)
			{
				delete userInput;
				throw msg;						// non-int input or other error
			}
		}
};

// Function Prototypes
void doWork (size_t instance, mutex *jobLock, Counter myCounter);

// Main
int main ()
{
	try
	{
		// Initialize Counter
		Counter myCounter = Counter ();

		// Declare Thread Variables
		thread workforce [MAXTHREADS];
		mutex jobLock;

		// Start Threads
		try
		{
			for (size_t worker = 0; worker < MAXTHREADS; ++worker)
			{
				workforce[worker] = thread (doWork, worker, &jobLock, myCounter);

				// Flip the Count
				if (myCounter.getDirection() == UP)
				{
					myCounter = Counter(DOWN, MAX);
				}
				else
				{
					myCounter = Counter(UP, MIN);
				}
			}
		}
		catch (const char* msg)
		{
			cerr << "Error Encountered: " << msg << endl;

			for (size_t i = 0; i < MAXTHREADS; ++i)
			{
				workforce[i].join();
			}

			cerr << "Joined Threads... Closing Program";

			return 0;
		}

		// Join Threads
		for (size_t i = 0; i < MAXTHREADS; ++i)
		{
			workforce[i].join();
		}

		return 0;
	}
	catch (const char* msg)
	{
		cerr << "Program Error: Join Failed - " << msg << endl;

		return 0;
	}
}

// Functions
void doWork (size_t instance, mutex *myJob, Counter myCounter)
{
	lock_guard <mutex> lock (*myJob);

	cout << "\n";
	cout << "Thread " << instance << " Locked" << endl;
	cout << "\n";

	if (myCounter.getDirection() == UP)
	{
		myCounter.countUp();
	}
	else
	{
		myCounter.countDown();
	}
}
