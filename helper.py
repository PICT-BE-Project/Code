# Example usage
class Base() : 

    def __init__(self ,data  ) -> None:
        self.data = data

    def encrypt(self , public_key) : 
        self.data  = [[public_key.encrypt(val) for val in row] for row  in self.data]
        self.all_labels = [public_key.encrypt(val) for val in self.all_labels]


class SampleDataset(Base) : 
    
    def __init__(self, data) -> None:
        super().__init__(data)

    def process(self)  : 
        self.all_labels = list(set(row[-1] for row in self.data))


class IrisDataset(Base) : 

    def __init__(self, dataset) -> None:
        super().__init__(dataset.data.tolist())


    def process(self ,dataset)  : 
        for i in range(len(self.data)):
            self.data[i].append(int(dataset.target[i]))   
        self.all_labels = list(set(row[-1] for row in self.data))


class BreastCancerDataset(Base) : 

    def __init__(self, data) -> None:
        super().__init__(data)
    
    def process(self)  : 
        self.data =  self.data.values.tolist()
        for row in self.data : 
            row[-1] = int(row[-1])
        self.all_labels = list(set(row[-1] for row in self.data))
        

class ArrhythmiaDataset(Base) : 

    def __init__(self, data) -> None:
        super().__init__(data)
    
    def process(self)  : 
        self.data =  self.data.values.tolist()
        for row in self.data : 
            row[-1] = int(row[-1])
        self.all_labels = list(set(row[-1] for row in self.data))


class CarDataset(Base) : 

    def __init__(self, data) -> None:
        super().__init__(data)
    
    def process(self)  : 
        self.data =  self.data.values.tolist()
        for row in self.data : 
            row[-1] = int(row[-1])
        self.all_labels = list(set(row[-1] for row in self.data))


