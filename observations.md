when rotor speed is low (<8) but not zero, it is randomly distributed with generally low wind, low power, and a random blade angle. This is becuase this only happens when the turbine is starting or stopping. It takes less than 10 minutes, so only a random point in the starting/stopping process is captured

removing stop statuses from kelmarsh data exclusively removed most (but not all) of this scattered data. So I think it is safe to cut it out completely

when writing and reading from csv it saves an index for reach row. when that gets fed into the KNN, it seems to just spread out the outliers. It appeared to make KNN more effective but SVMKNN worse