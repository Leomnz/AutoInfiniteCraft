# Auto Infinite Craft
An automated selenium web tool to do programmatic combinations in Infinte Craft and save the results as a directed graph.


## Installation
Use python 3.10
```bash
git clone https://github.com/Leomnz/AutoInfiniteCraft
cd AutoInfiniteCraft
pip install -r requirements.txt
```
    
## Graphs
Graphs are saved in gml format and visualized with networkx
![demo1](https://github.com/Leomnz/AutoInfiniteCraft/blob/d9a712c4087837d0d5bd62182ae8eafcf5aedd2e/images/image1.png)

![demo2](https://github.com/Leomnz/AutoInfiniteCraft/blob/d9a712c4087837d0d5bd62182ae8eafcf5aedd2e/images/image2.png)
Can be rendered in any program that supports gml once there are too many nodes to be rendered automatically.

## Known issues
does not detect 403 response from the server after getting blocked.
