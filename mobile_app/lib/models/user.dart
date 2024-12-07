class User {
  final String id;
  final String email;
  final int knowledgeLevel;

  User({required this.id, required this.email, required this.knowledgeLevel});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      knowledgeLevel: json['knowledge_level'],
    );
  }
}