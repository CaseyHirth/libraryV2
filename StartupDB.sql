INSERT INTO ``.`jobs` (`id`, `job_title`, `job_description`) VALUES ('1', 'Employee', 'Library employee');
INSERT INTO ``.`jobs` (`id`, `job_title`, `job_description`) VALUES ('2', 'Branch Manager', 'Manader of a library branch');
INSERT INTO ``.`jobs` (`id`, `job_title`, `job_description`) VALUES ('3', 'Region Manager', 'Manages of a library region');

INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('1', 'admin@email.com', 'Admin', 'Admin', '1', '158 38th St', 'PA', 'Pittsburgh', '15201');
INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('2', 'josezindia36@gmail.com', 'Jose', 'Zindia', '3', '1000 Fifth Ave', 'PA', 'Pittsburgh', '15213');
INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('3', 'andyadams@gmail.com', 'Andy', 'Adams', '2', '2000 Fifth Ave', 'PA', 'Pittsburgh', '15213');
INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('4', 'cindysmith@yahoo.com', 'Cindy', 'Smith', '2', '4000 Apple Dr', 'OH', 'Cleveland', '12345');
INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('5', 'rachelwillis@', 'Rachel', 'Willis', '2', '5000 Orange Dr', 'OH', 'Youngstown', '12345');
INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('6', 'johnhine@gmail.com', 'John', 'Hine', '2', '300 Shadow Ln', 'PA', 'Monroeville', '12342');
INSERT INTO ``.`employees` (`id`, `email`, `firstName`, `lastName`, `job_id`, `street`, `state`, `city`, `zip`) VALUES ('7', 'normbase@gmail.com', 'Norm', 'Base', '1', '100 Pittsburgh Dr', 'PA', 'Pittsburgh', '15201');

INSERT INTO ``.`users` (`id`, `email`, `password`, `role`) VALUES ('3', 'admin@email.com', 'sha256$s4kbDTAh$7143b9affb5ab23a123ab7528aebbc4eb0be4e5fe56b353385c669125b77650b', 'employee');

INSERT INTO ``.`regions` (`id`, `regionName`, `regionManager`) VALUES ('1', 'South West PA', '1');
INSERT INTO ``.`regions` (`id`, `regionName`, `regionManager`) VALUES ('2', 'Western Ohio', '2');

INSERT INTO ``.`branchs` (`id`, `branchName`, `street`, `state`, `city`, `zip`, `branch_manager_id`, `region_id`) VALUES ('1', 'Pittsburgh', '1000 Forbes Ave', 'PA', 'Pittsburgh', '15213', '3', '1');
INSERT INTO ``.`branchs` (`id`, `branchName`, `street`, `state`, `city`, `zip`, `branch_manager_id`, `region_id`) VALUES ('2', 'Monroeville', '1000 Sandy Dr', 'PA', 'Monroeville', '16781', '6', '1');
INSERT INTO ``.`branchs` (`id`, `branchName`, `street`, `state`, `city`, `zip`, `branch_manager_id`, `region_id`) VALUES ('3', 'Cleveland', '2000 Cuyahoga Dr', 'OH', 'Cleveland', '12345', '4', '2');
INSERT INTO ``.`branchs` (`id`, `branchName`, `street`, `state`, `city`, `zip`, `branch_manager_id`, `region_id`) VALUES ('4', 'Youngstown', '123 Industry Ave', 'OH', 'Youngstown', '15143', '5', '2');
