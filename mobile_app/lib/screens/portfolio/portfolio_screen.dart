import 'package:flutter/material.dart';

class PortfolioScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('My Portfolio')),
      body: Center(
        child: Text('Portfolio Content Coming Soon'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Implement create portfolio
        },
        child: Icon(Icons.add),
      ),
    );
  }
}