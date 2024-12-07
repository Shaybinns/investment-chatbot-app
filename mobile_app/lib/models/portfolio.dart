class Portfolio {
  final String id;
  final String name;
  final double riskLevel;
  final List<Asset> assets;

  Portfolio({
    required this.id,
    required this.name,
    required this.riskLevel,
    required this.assets,
  });
}

class Asset {
  final String symbol;
  final double allocation;

  Asset({required this.symbol, required this.allocation});
}