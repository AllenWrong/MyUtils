## Visualize 2d-array util

**Version 1.0** 

Main class `TableVis`:

- Input: 

  - A 2d-array: can be String or Integer. This is required.
  - A table head:  this is optional.

- Output: Looking like the following format.

  ```
  +--------+--------------+--------+------------+------------+
  | bookid | Rno          | isback | borrowDate | backDate   |
  +--------+--------------+--------+------------+------------+
  | O1-7   | 201711010144 | 否     | 2019-06-12 | 2019-07-12 |
  | TP-0-5 | 201711010102 | 否     | 2019-06-12 | 2019-07-12 |
  | TP-0-5 | 201711010144 | 否     | 2019-06-12 | 2019-07-12 |
  | TP-0-8 | 201711010144 | 否     | 2019-06-12 | 2019-07-12 |
  +--------+--------------+--------+------------+------------+
  ```

`Test` class is a demo which how you can use this class. 