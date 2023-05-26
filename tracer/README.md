# Трассировка автономных систем
Эта программа выполняет трассировку до указанного узла, который может быть IP-адресом или доменным именем. 

## Входные данные

**help:** python tracer.py -h

**input:** python tracer.py target, где target - IP-адрес или доменное имя
  
**output:** таблица вида *№ | IP | AS | Country | Provider*, где № - номер перехода, IP - IP адрес, AS - номер автономной системы, Country - страна, Provider - провайдер для каждого IP-адреса, прослеживаемого при трассировке.

## Пример использования

<img width="568" alt="Снимок экрана 2023-04-14 в 18 08 32" src="https://user-images.githubusercontent.com/91218615/232052640-e7707e0f-820b-4528-acff-53d8f5263eb1.png">

<img width="565" alt="Снимок экрана 2023-04-14 в 18 21 40" src="https://user-images.githubusercontent.com/91218615/232055325-1bcd1a60-8f11-4035-87d7-486025a0e5df.png">
