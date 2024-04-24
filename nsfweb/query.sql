use smartfactory;
create database smartfactory;

create table ProductClassificationLog (
	ProductClassificationLogID INT AUTO_INCREMENT PRIMARY KEY,
    StartTime datetime,
    PauseTime datetime,
    FinishTime datetime,
    Status char(1),
    GoalRedCnt int,
    GoalGreenCnt int,
    GoalBlueCnt int,
    GoalYellowCnt int,
    ProductRedCnt int,
    ProductGreenCnt int,
    ProductBlueCnt int,
    ProductYellowCnt int,
    ErrorEdgeCnt int,
    ErrorColorCnt int,
    ErrorQrCnt int,
    ErrorImageCnt int
);

select * from ProductClassificationLog order by ProductClassificationLogID desc;
