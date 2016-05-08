# xsd2dbschemagen

The script takes as input the starting type in an xsd and drill down the hierarchy listing all the nodes from that root. In the process it appends the name at each level.

For example if an XSD is as given below and starting root is a it will output

	a
	 b
        1
        2
     c
        3
        4
     d
        5
          p
            q

	ab1
	ab2
	ac3
	ac4
	ad5pq