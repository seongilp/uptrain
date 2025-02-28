<h1 align="center">
  <a href="https://uptrain.ai">
    <img width="300" src="https://user-images.githubusercontent.com/108270398/214240695-4f958b76-c993-4ddd-8de6-8668f4d0da84.png" alt="uptrain">
  </a>
</h1>

<h1 style="text-align: center;">Performance Monitoring: Fraud Detection</h1>

**Overview**: In this example, we see how to use UpTrain to monitor performance of a fraud detection task. For the same, we will be training a binary classifier on a popular network traffic dataset called the [NSL-KDD dataset](https://www.unb.ca/cic/datasets/nsl.html) for cyber-attack classification using the [XGBoost classifier](https://xgboost.readthedocs.io/en/stable/). 

**Dataset**: The NSL-KDD dataset includes a variety of network attack types, including denial-of-service (DoS) attacks, unauthorized access (U2R) attacks, and probe attacks. The dataset contains a total of around 25,000 instances and 41 different features that describe the behavior of network connections, such as the number of failed login attempts and the size of packets transmitted.

**Why is monitoring needed**: Once our fraud detection model has been trained, it may initially perform well in detecting malicious activity. However, over time, attackers may adapt their tactics and evolve their methods, leading to a mismatch between the type of attacks seen during training and those seen in production. This can result in decreased accuracy in our model's predictions.

**Solution**: We will be using UpTrain framework which provides an easy-to-configure way to log model predictions and attach ground-truth to monitor model's performance. We are using drift detection methon on top on model performance to raise alerts in case of any dip in model's accuracy, commonly called **Concept Drift.**

## Step 1: Let's download and prepare the NSL-KDD dataset

#### Let's read the data and see how it looks


    Labels for first few rows:
    [0, 0, 1, 0, 0] 
    
    Input features for first few rows:





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>duration</th>
      <th>protocol_type</th>
      <th>service</th>
      <th>flag</th>
      <th>src_bytes</th>
      <th>dst_bytes</th>
      <th>land</th>
      <th>wrong_fragment</th>
      <th>urgent</th>
      <th>hot</th>
      <th>...</th>
      <th>dst_host_count</th>
      <th>dst_host_srv_count</th>
      <th>dst_host_same_srv_rate</th>
      <th>dst_host_diff_srv_rate</th>
      <th>dst_host_same_src_port_rate</th>
      <th>dst_host_srv_diff_host_rate</th>
      <th>dst_host_serror_rate</th>
      <th>dst_host_srv_serror_rate</th>
      <th>dst_host_rerror_rate</th>
      <th>dst_host_srv_rerror_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>20</td>
      <td>9</td>
      <td>491</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>150</td>
      <td>25</td>
      <td>0.17</td>
      <td>0.03</td>
      <td>0.17</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.05</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>2</td>
      <td>44</td>
      <td>9</td>
      <td>146</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>255</td>
      <td>1</td>
      <td>0.00</td>
      <td>0.60</td>
      <td>0.88</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>1</td>
      <td>49</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>255</td>
      <td>26</td>
      <td>0.10</td>
      <td>0.05</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>1.00</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>1</td>
      <td>24</td>
      <td>9</td>
      <td>232</td>
      <td>8153</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>30</td>
      <td>255</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>0.03</td>
      <td>0.04</td>
      <td>0.03</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>1</td>
      <td>24</td>
      <td>9</td>
      <td>199</td>
      <td>420</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>255</td>
      <td>255</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 41 columns</p>
</div>



#### Divide the data into training and test sets
We use first 10% of the data to train and 90% of the data to evaluate the model in production


```python
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-1].values, df.iloc[:, -1].values,
                                                    test_size = 0.9, 
                                                    random_state = 0,
                                                    shuffle=False)

print("Num Training samples: ", str(len(X_train)) + ",", " Num Testing samples: ", len(X_test))
```

    Num Training samples:  14851,  Num Testing samples:  133666


## Step 2: Train our XGBoost Classifier


```python
# Train the XGBoost classifier with training data
classifier = XGBClassifier()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_train)
print("Training accuracy: " + str(100*accuracy_score(y_train, y_pred)))
```

    Training accuracy: 100.0


Woah! 😲🔥 The training accuracy is 100%. Let's see how long the model lasts in production. 

## Step 3: Monitoring model performance using UpTrain


```python
cfg = {
    # Checks to identify concept drift
    "checks": [{
        'type': uptrain.Anomaly.CONCEPT_DRIFT,
        'algorithm': uptrain.DataDriftAlgo.DDM
    }],
    
    # Folder that stores the drifted data-points identified by UpTrain
    "retraining_folder": 'uptrain_smart_data',
    
    # Enable streamlit logging to visualize model's performance
    "st_logging": True,
}
pretty(cfg)
```

    - checks:
    	- type:
    		Anomaly.CONCEPT_DRIFT
    	- algorithm:
    		DataDriftAlgo.DDM
    - retraining_folder:
    	uptrain_smart_data
    - st_logging:
    	True



```python
# Initialize the UpTrain framework
framework = uptrain.Framework(cfg)

batch_size = 10000
for i in range(int(len(X_test)/batch_size)):
    
    # Do model prediction
    inputs = {'data': {"feats": X_test[i*batch_size:(i+1)*batch_size]}}
    preds = classifier.predict(inputs['data']["feats"])
    
    # Log model inputs and outputs to monitor concept drift
    ids = framework.log(inputs=inputs, outputs=preds)
    
    # Attach ground truth to corresponding predictions 
    # in UpTrain framework and identify concept drift
    ground_truth = y_test[i*batch_size:(i+1)*batch_size] 
    framework.log(identifiers=ids, gts=ground_truth)
    
    # Pausing between batches to monitor progress in the dashboard
    time.sleep(0.5)
```
                
    Drift detected with DDM at time: 111298!!!


As can be noted from the dashboard, we start seeing a sharp dip in model's accuracy around the timestamp of 111k.

<img width="629" alt="concept_drift_avg_acc" src="https://user-images.githubusercontent.com/5287871/216795937-7e3e0609-6053-4256-956d-c07de3b7d73e.png">

In the this example, we used a popular drift detection algorithm called the [Drift Detection Method (DDM)](https://riverml.xyz/0.11.1/api/drift/DDM/) which is already implemented as a part of the UpTrain package. However, as we see the model accuracy is dropping from 99.7% to 96.9% which is still a slow decline but not might raise many eyebrows. 

For better detection and understanding the severity of the issue, one might want to define a customized metric and monitor the models using them. Let's see how to do that in UpTrain.

## Step 4: Define a Custom Monitor in UpTrain (for better monitoring)

We now define a custom drift metric which monitors the difference between accuracy of the model on the first 200 predictions and the most recent 200 predictions. This way, they can quickly identify if there was a sudden degradation in the model performance.

Let's define our custom check and UpTrain config with check as "Custom Monitor" as below:


```python
"""
Defining a custom drift metric to check if accuracy drops beyond a threshold.
"""

def custom_initialize_func(self):
    self.initial_acc = None       
    self.acc_arr = []
    self.count = 0       
    self.thres = 0.02
    self.window_size = 200
    self.is_drift_detected = False

def custom_check_func(self, inputs, outputs, gts=None, extra_args={}):
    batch_size = len(extra_args["id"])
    self.count += batch_size
    self.acc_arr.extend(list(np.equal(gts, outputs)))
    
    # Calculate initial performance of the model on first 200 points
    if (self.count >= self.window_size) and (self.initial_acc is None):
        self.initial_acc = sum(self.acc_arr[0:self.window_size])/self.window_size
        
    # Calculate the most recent accuracy and log it to dashboard.
    if (self.initial_acc is not None):
        for i in range(self.count - batch_size, self.count, self.window_size):
            
            # Calculate the most recent accuracy
            recent_acc = sum(self.acc_arr[i:i+self.window_size])/self.window_size
            
            # Logging to UpTrain dashboard
            self.log_handler.add_scalars('custom_metrics', {
                    'initial_acc': self.initial_acc,
                    'recent_acc': recent_acc,
                }, i, self.dashboard_name)
            
            # Send an alert when recent model performance goes down 
            if (self.initial_acc - recent_acc > self.thres) and (not self.is_drift_detected):
                alert = f"Concept drift detected with custom metric at time: {i}!!!" 
                print(alert)
                self.log_handler.add_alert(
                    "Model Performance Degradation Alert 🚨",
                    alert,
                    self.dashboard_name
                )
                self.is_drift_detected = True

cfg = {
    # Checks for our custom monitor
    "checks": [{
        'type': uptrain.Anomaly.CUSTOM_MONITOR,
        'initialize_func': custom_initialize_func,
        'check_func': custom_check_func,
        'need_gt': True,
    }],
    
    # Folder that stores the drifted data-points identified by UpTrain
    "retraining_folder": 'uptrain_smart_data',
    
    # Enable streamlit logging to visualize model's performance
    "st_logging": True,
}
pretty(cfg)
```

    - checks:
    	- type:
    		Anomaly.CUSTOM_MONITOR
    	- initialize_func:
    		<function custom_initialize_func at 0x154a29750>
    	- check_func:
    		<function custom_check_func at 0x154a29900>
    	- need_gt:
    		True
    - retraining_folder:
    	uptrain_smart_data
    - st_logging:
    	True



```python
# Initialize the UpTrain framework
framework = uptrain.Framework(cfg)

batch_size = 10000
for i in range(int(len(X_test)/batch_size)):
    
    # Do model prediction
    inputs = {'data': {"feats": X_test[i*batch_size:(i+1)*batch_size]}}
    preds = classifier.predict(inputs['data']["feats"])
    
    # Log model inputs and outputs to monitor concept drift
    ids = framework.log(inputs=inputs, outputs=preds)
    
    # Attach ground truth to corresponding predictions 
    # in UpTrain framework and identify concept drift
    ground_truth = y_test[i*batch_size:(i+1)*batch_size] 
    framework.log(identifiers=ids, gts=ground_truth)
    
    # Pausing between batches to monitor progress in the dashboard
    time.sleep(0.5)
```

    Concept drift detected with custom metric at time: 111000!!!


As we see, we see a sudden (and more alarming) drop using our custom monitors. We can clearly see that the model accuracy drops from 99.7% to 77%, enabling us to send better alerts and take more urgent measures (ex: model retraining) to solve them. 

<img width="624" alt="concept_drift_custom" src="https://user-images.githubusercontent.com/5287871/216795956-a35bcd9f-8b60-439d-9ea2-8e19854390bb.png">

## Conclusion

Model monitoring is very crucial for tasks such as fraud detection, cyber-security attacks, etc. and where the attackers continuously improve their attack vectors and with time learn to evade detection. Real-time model observability enables one to proactively address any performance degradation before it leads to serious consequences, such as hacks or financial loss.

In this example, we saw two ways to detect performance degradation - Concept Drift via DDM and Custom monitor. The UpTrain framework has many other statistical tools, such as data drift, integrity checks, shift in model outputs, and outlier detection, that can be used to identify model issues, even in cases where ground truth is not available. You can explore them [here](https://github.com/uptrain-ai/uptrain/tree/main/examples)

- Automatically detecting edge-cases and out-of-distribution samples - [Link](https://github.com/uptrain-ai/uptrain/blob/improve_cyber_attack_example/examples/human_orientation_classification/run.ipynb)
- Defining custom signals to identify edge-cases - [Link](https://github.com/uptrain-ai/uptrain/blob/improve_cyber_attack_example/examples/human_orientation_classification/deepdive_examples/uptrain_edge_cases_torch.ipynb)
- Using Data-Drift (i.e. shifts in input distribution) to identify dips in model performance - Coming soon
- Monitoring bias in recommendation systems - [Link](https://github.com/uptrain-ai/uptrain/blob/improve_cyber_attack_example/examples/shopping_cart_recommendation/run.ipynb)
