---
title: What is Feature Engineering in Machine Learning?
module: 1
module_title: Machine Learning Foundations
lesson: '1.4'
source: https://outcomeschool.com/blog/feature-engineering
published: August 2, 2019
tags:
- ai
- machine-learning
videos:
- title: Feature Engineering in Machine Learning
  url: https://www.youtube.com/watch?v=QLlywrWuXag
- title: One-hot Encoding in Machine Learning
  url: https://www.youtube.com/watch?v=6AmedU5i9go
fetched: '2026-10-24'
words: 934
reading_time: 5
status: full
---
# What is Feature Engineering in Machine Learning?

> **Module 1 · Lesson 1.4**  
> Source: [Outcome School](https://outcomeschool.com/blog/feature-engineering) · Published: August 2, 2019 · Reading time: ~5 min · Tags: `ai`, `machine-learning`
> Video: [Feature Engineering in Machine Learning](https://www.youtube.com/watch?v=QLlywrWuXag)
> Video: [One-hot Encoding in Machine Learning](https://www.youtube.com/watch?v=6AmedU5i9go)

---

![Feature Engineering for Machine Learning](../../assets/images/01-01-04-what-is-feature-engineering-in-machine-learning/feature-engineering.png)

Feature Engineering is the process of using domain knowledge of the data to create features that make Machine Learning algorithms work. If it is done correctly, it increases the predictive power of the model.

In this blog, we will learn about the Feature Engineering for Machine Learning.

Let's get started.

**Feature Engineering is an art**

Feature engineering is the process of using **domain knowledge** of the data to create features that make [machine learning](https://outcomeschool.com/blog/machine-learning) algorithms work. If feature engineering is done correctly, it increases the predictive power of machine learning algorithms by creating features from raw data that help facilitate the machine learning process. Feature Engineering is an art.

**Steps which are involved while solving any problem in machine learning are as follows:**

- Gathering data.
- Cleaning data.
- **Feature engineering**.
- Defining model.
- Training, testing model and predicting the output.

Feature engineering is the most important art in machine learning which creates the huge difference between a good model and a bad model. Let's see what feature engineering covers.

Suppose, we are given a data "flight date time vs status". Then, given the date-time data, we have to predict the status of the flight.

|  | Date\_Time\_Combined | Status |
| --- | --- | --- |
| 0 | 2018-02-14 20:40 | Delayed |
| 1 | 2018-02-15 10:30 | On Time |
| 2 | 2018-02-14 07:40 | On Time |
| 3 | 2018-02-15 18:10 | Delayed |
| 4 | 2018-02-14 10:20 | On Time |

As the status of the flight depends on the hour of the day, not on the date-time. We will create the new feature `Hour_Of_Day`. Using the `Hour_Of_Day` feature, the machine will learn better as this feature is directly related to the status of the flight.

|  | Hour\_Of\_Day | Status |
| --- | --- | --- |
| 0 | 20 | Delayed |
| 1 | 10 | On Time |
| 2 | 7 | On Time |
| 3 | 18 | Delayed |
| 4 | 10 | On Time |

Here, creating the new feature `Hour_Of_Day` is the feature engineering.

Let's see another example. Suppose we are given the latitude, longitude and other data with the given label `Price_Of_House`. We need to predict the price of the house in that area. The latitude and longitude are not of any use if they are alone. So, here we will use the **crossed column** feature engineering. We will combine the latitude and the longitude to make one feature. Combining into one feature will help the model learn better.

Here, combining two features to create one useful feature is the feature engineering.

Sometimes, we use the **bucketized column** feature engineering. Suppose we are given a data in which one column is the age and the output is the classification(X, Y, Z). By seeing the data, we realized that the output(X, Y, Z) is dependent on the age-range like 11-20 years age-range output to X, 21-40 years output to Y, 41-70 years output to Z. Here, we will create 3 buckets for the age-range 11-20, 21-40 and 41-70. We will create the new feature which is the bucketized column `Age_Range` having the numerical values 1, 2 and 3 where 1 is mapped to the bucket 1, 2 is mapped to the bucket 2 and 3 is mapped to the bucket 3.

Here, creating `Age_Range` bucket is the feature engineering.

Sometimes, removing the unwanted feature is also feature engineering. As the feature which is not related degrade the performance of the model.

**Now, the steps to do feature engineering are as follows:**

- Brainstorm features.
- Create features.
- Check how the features work with the model.
- Start again from first until the features work perfectly.

This is what we do in the feature engineering.

**Some words on feature engineering by the experts**

> Feature engineering is another topic which doesn’t seem to merit any review papers or books, or even chapters in books, but it is absolutely vital to ML success. Much of the success of machine learning is actually success in engineering features that a learner can understand.

> Actually the success of all Machine Learning algorithms depends on how you present the data.

> The algorithms we used are very standard for Kagglers. We spent most of our efforts in feature engineering.

> Feature engineering is the process of transforming raw data into features that better represent the underlying problem to the predictive models, resulting in improved model accuracy on unseen data.

> Feature engineering turn your inputs into things the algorithm can understand.

Last but not least, **Automated Feature Engineering** is the current hot topic. But it requires a lot of resources. Few companies have already started working on it.

## Frequently Asked Questions

### Is removing features also part of feature engineering?

Yes. Removing an unwanted feature is also feature engineering. A feature that is not related to the output can degrade the performance of the model. So, along with creating new features, we should also drop the ones that do not help.

### Where does feature engineering fit in a machine learning project?

Feature engineering comes after gathering and cleaning the data, and before defining the model. After it, we train and test the model and predict the output. It is the step that creates the huge difference between a good model and a bad model.

### What is a crossed column in feature engineering?

A crossed column combines two features into one useful feature. For example, latitude and longitude are not of much use alone when we want to predict the price of a house. Combining them into one feature helps the model learn better.

### Can feature engineering be automated?

Yes. Automated Feature Engineering is a current hot topic, and a few companies have already started working on it. But it requires a lot of resources.
