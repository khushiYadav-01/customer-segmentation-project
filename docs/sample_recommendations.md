# Sample Recommendation Output

## 1. Item-based: "Customers who bought X also bought..."

**Air Fryer**
  - Electric Kettle  (similarity: 0.400)
  - Cushion Cover Set  (similarity: 0.398)
  - Wall Clock Pro  (similarity: 0.372)
  - Electric Kettle Pro  (similarity: 0.363)
  - Knife Set  (similarity: 0.363)

**Air Fryer Pro**
  - Ceramic Mug Set  (similarity: 0.445)
  - Denim Jacket Pro  (similarity: 0.402)
  - Sticky Notes Pro  (similarity: 0.393)
  - LED Desk Lamp  (similarity: 0.391)
  - Cushion Cover Set  (similarity: 0.389)

**Analog Watch**
  - Leather Wallet Pro  (similarity: 0.454)
  - Backpack  (similarity: 0.398)
  - Lipstick  (similarity: 0.396)
  - Sunscreen  (similarity: 0.362)
  - Face Wash  (similarity: 0.357)

## 2. Personalized recommendations per customer

**Customer C0001**
  - Planner Diary Pro  (score: 4.549)
  - Formal Shirt  (score: 4.386)
  - Face Wash  (score: 4.347)
  - Puzzle Book Pro  (score: 4.303)
  - Fiction Novel  (score: 4.299)

**Customer C0002**
  - Fountain Pen Pro  (score: 13.465)
  - Mechanical Keyboard  (score: 13.233)
  - Planner Diary Pro  (score: 12.979)
  - Power Bank  (score: 12.887)
  - Sunscreen Pro  (score: 12.863)

**Customer C0003**
  - Backpack Pro  (score: 5.104)
  - Formal Shirt  (score: 5.085)
  - Wall Clock Pro  (score: 4.910)
  - Denim Jacket Pro  (score: 4.899)
  - Trimmer Pro  (score: 4.892)

## 3. Top association rules (market basket)

| Antecedent | Consequent | Support | Confidence | Lift |
|---|---|---|---|---|
| Cushion Cover Set Pro | LED Desk Lamp | 0.0037 | 0.158 | 6.81 |
| LED Desk Lamp | Cushion Cover Set Pro | 0.0037 | 0.159 | 6.81 |
| Puzzle Book | Notebook Set | 0.0046 | 0.165 | 6.17 |
| Notebook Set | Puzzle Book | 0.0046 | 0.173 | 6.17 |
| Smart Watch | USB-C Cable | 0.0039 | 0.155 | 6.17 |
| USB-C Cable | Smart Watch | 0.0039 | 0.156 | 6.17 |
| Storage Boxes Pro | Electric Kettle Pro | 0.0040 | 0.150 | 6.16 |
| Electric Kettle Pro | Storage Boxes Pro | 0.0040 | 0.166 | 6.16 |
| Ceramic Mug Set | Air Fryer Pro | 0.0039 | 0.163 | 6.10 |
| Air Fryer Pro | Ceramic Mug Set | 0.0039 | 0.147 | 6.10 |