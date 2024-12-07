import 'package:flutter/material.dart';

void main() {
  runApp(InvestmentChatbotApp());
}

class InvestmentChatbotApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Investment Chatbot',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Investment Chatbot'),
      ),
      body: Center(
        child: Text('Welcome to Investment Chatbot'),
      ),
    );
  }
}