import 'package:flutter/material.dart';

class OnboardingScreen extends StatefulWidget {
  @override
  _OnboardingScreenState createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  int _currentPage = 0;
  final _questions = [
    'What is your investment experience?',
    'What are your investment goals?',
    'What is your risk tolerance?',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(_questions[_currentPage],
                  style: Theme.of(context).textTheme.headline6),
              // TODO: Implement question answers
              ElevatedButton(
                onPressed: () {
                  // TODO: Implement next/finish logic
                },
                child: Text(_currentPage < _questions.length - 1 ? 'Next' : 'Finish'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}