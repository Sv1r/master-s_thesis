# Моделирование полей напряжений при помощи нейронной сети

## Аннотация

Математическое моделирование напряженно-деформированного состояние в механике твердых тел как правило осуществляется при помощи численного [**Метода Конечных Элементов**](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%BA%D0%BE%D0%BD%D0%B5%D1%87%D0%BD%D1%8B%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2) ([*Finite Element Method*](https://en.wikipedia.org/wiki/Finite_element_method)), однако данный   подход является крайне *дорогим* с точки зрения вычислений, так как требует формирования сетки конечных элементов, а затем последующего численного решения дифференциального уравнения на ее основе. 

В данной работе я попробую использовать иной подход для формирования полей напряжений на примере композитного материала с цилиндрическими включениями различного радиуса при помощи подхода, основанного на глубоком обучении. Данные для текущего проекта были сформированы при помощи программы [**Abaqus**](https://www.3ds.com/products-services/simulia/products/abaqus/) с использование рандомизированной геометрии образцов.

На данную работу меня вдохновил ряд статей по схожей тематике:

- [Stress field prediction in fiber-reinforced composite materials using a deep learning approach](https://arxiv.org/pdf/2111.05271.pdf)
- [Deep learning prediction of stress fields in additively manufactured metals with intricate defect networks](https://arxiv.org/ftp/arxiv/papers/2105/2105.10564.pdf)
- [A deep learning framework for solution and discovery in solid mechanics](https://arxiv.org/pdf/2003.02751.pdf)
- [StressNet: Deep Learning to Predict Stress With Fracture Propagation in Brittle Materials](https://arxiv.org/pdf/2011.10227v1.pdf)
- [Bayesian convolutional neural networks as probabilistic surrogates for the fast prediction of stress fields in structures with microscale features](https://arxiv.org/pdf/2012.11330v1.pdf)

Использованная мной нейронной сети основывается на архитектуре **Pix2Pix**, которая была впервые представленна в статье [Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/pdf/1611.07004.pdf).
