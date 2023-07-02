<?php 

class search_controller{
    public bool $isFound;
    public array | string | object $results;
    protected array $error;
    public function __construct()
    {
        $this->isFound = false;
    }
    public function search(string $query)
    {
            $cSession = curl_init(); 
            curl_setopt($cSession,CURLOPT_URL, "https://api.yoguide.info/search?q=$query");
            curl_setopt($cSession,CURLOPT_RETURNTRANSFER,true);
            $resp = curl_exec($cSession);

            if($resp == "[ X ] Unable to find item.....!")
            {
                $this->isFound == false;
                $this->results = "Nothing Found In Here";
                return $this->isFound;
            }
            $this->isFound = true;
            $this->results = $resp;
            return $this->isFound;

    }
    public function fetch()
    {
        if(!empty($this->results))
        {
            $sets = explode("]", $this->results);
            $sets = str_replace(["["], '', $sets);

            $result = array_map(function($set) {
                return explode(',', $set, 3);
            }, $sets);
            return $result;

        }
        return false;
    }

    
}