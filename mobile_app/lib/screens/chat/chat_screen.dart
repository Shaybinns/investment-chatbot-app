import 'package:flutter/material.dart';

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _messages = [];
  final _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Assistant')),
      body: Column(
        children: [
          Expanded(child: ListView.builder(
            itemCount: _messages.length,
            itemBuilder: (context, index) => ListTile(
              title: Text(_messages[index].toString()),
            ),
          )),
          _buildInputField(),
        ],
      ),
    );
  }

  Widget _buildInputField() {
    return Padding(
      padding: EdgeInsets.all(8.0),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: InputDecoration(hintText: 'Type a message...'),
            ),
          ),
          IconButton(
            icon: Icon(Icons.send),
            onPressed: () {
              // TODO: Implement send message
            },
          ),
        ],
      ),
    );
  }
}